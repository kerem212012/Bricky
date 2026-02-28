"""Views for orders app.

Handles shopping cart operations, checkout process, order creation,
and order history management.
"""
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from decimal import Decimal
import logging

from store.models import Product
from orders.models import Cart, CartItem, Customer, Order, OrderElement, Delivery


# ===== Cart Views =====

class CartView(LoginRequiredMixin, TemplateView):
    """Display user's shopping cart with items and totals.
    
    Shows cart items, prices, shipping cost, and grand total.
    Requires authentication.
    """
    template_name = 'orders/cart/cart.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        """Get context data for cart view.
        
        Returns:
            Context dictionary with cart items and totals
        """
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        
        shipping_cost = self._get_shipping_cost()
        
        context.update({
            'cart': cart,
            'cart_items': cart.items.select_related('product'),
            'total_price': cart.get_total_price(),
            'total_items': cart.get_total_items(),
            'shipping_cost': shipping_cost,
            'grand_total': cart.get_total_price() + shipping_cost
        })
        
        return context
    
    def _get_shipping_cost(self):
        """Helper to get shipping cost from session"""
        try:
            return Decimal(self.request.session.get('shipping_cost', '10.00'))
        except Exception:
            return Decimal('10.00')


class CartActionView(View):
    """Base class for cart action views.
    
    Provides common functionality:
    - Authentication checking
    - Cart retrieval
    - Standardized JSON responses
    
    Used by: AddToCartView, RemoveFromCartView, UpdateCartItemView, ClearCartView
    """
    
    def dispatch(self, request, *args, **kwargs):
        """Check authentication before processing request.
        
        Returns 401 JSON response if user is not authenticated.
        
        Args:
            request: HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Response from parent class or 401 error
        """
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Please log in to manage cart',
                'requires_login': True
            }, status=401)
        return super().dispatch(request, *args, **kwargs)
    
    def get_cart(self):
        """Get or create cart for current user.
        
        Returns:
            Cart object for authenticated user
        """
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    def cart_response(self, success=True, message='', **extra):
        """Generate standardized cart response JSON.
        
        Args:
            success: Whether operation was successful (default: True)
            message: Message to include in response (default: '')
            **extra: Additional data to include in response
            
        Returns:
            JsonResponse with standardized format
        """
        cart = self.get_cart()
        response = {
            'success': success,
            'message': message,
            'cart_count': cart.get_total_items(),
            'cart_total': str(cart.get_total_price()),
        }
        response.update(extra)
        return JsonResponse(response, status=200 if success else 400)


class AddToCartView(CartActionView):
    """Add product to shopping cart.
    
    AJAX endpoint that validates stock, creates or updates cart item.
    Returns JSON with success status and updated cart totals.
    """

    def post(self, request, *args, **kwargs):
        """Handle add to cart request.
        
        Validates product and quantity, updates cart, returns JSON response.
        
        Args:
            request: HTTP request with POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            JsonResponse with success status and updated cart info
        """
        try:
            product_id = request.POST.get('product_id')
            
            # Validate quantity
            try:
                quantity = int(request.POST.get('quantity', 1))
                if quantity < 1:
                    raise ValueError
            except (ValueError, TypeError):
                return self.cart_response(False, 'Invalid quantity')
            
            # Get product
            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                return self.cart_response(False, 'Product not found')
            
            # Check stock
            if product.stock < quantity:
                return self.cart_response(
                    False, 
                    f'Only {product.stock} items available'
                )
            
            # Add to cart
            cart = self.get_cart()
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'price': product.price, 'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return self.cart_response(
                True, 
                f'{product.name} added to cart',
                requires_login=False
            )
        
        except Exception as e:
            logging.getLogger(__name__).error(f'Cart error: {e}', exc_info=True)
            return self.cart_response(False, 'An error occurred')


class RemoveFromCartView(CartActionView):
    """Remove item from shopping cart.
    
    AJAX endpoint that deletes cart item by ID.
    Returns JSON with success status and updated cart totals.
    """

    def post(self, request, *args, **kwargs):
        """Handle remove from cart request.
        
        Deletes cart item by ID, returns JSON response.
        
        Args:
            request: HTTP request with POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            JsonResponse with success status
        """
        try:
            cart_item_id = request.POST.get('cart_item_id')
            if not cart_item_id:
                return self.cart_response(False, 'Cart item ID required')
            
            cart_item = CartItem.objects.get(
                id=cart_item_id, 
                cart__user=request.user
            )
            product_name = cart_item.product.name
            cart_item.delete()
            
            return self.cart_response(True, f'{product_name} removed')
        
        except CartItem.DoesNotExist:
            return self.cart_response(False, 'Item not found')
        except Exception as e:
            return self.cart_response(False, str(e))


class UpdateCartItemView(CartActionView):
    """Update cart item quantity via AJAX"""

    def post(self, request, *args, **kwargs):
        """Handle update cart item quantity request.
        
        Updates item quantity or removes if quantity < 1.
        
        Args:
            request: HTTP request with POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            JsonResponse with success status
        """
        try:
            cart_item_id = request.POST.get('cart_item_id')
            
            # Validate quantity
            try:
                quantity = int(request.POST.get('quantity', 1))
            except (ValueError, TypeError):
                return self.cart_response(False, 'Invalid quantity')
            
            cart_item = CartItem.objects.get(
                id=cart_item_id,
                cart__user=request.user
            )
            
            # Remove if quantity < 1
            if quantity < 1:
                cart_item.delete()
                return self.cart_response(True, 'Item removed')
            
            # Check stock
            if cart_item.product.stock < quantity:
                return self.cart_response(
                    False,
                    f'Only {cart_item.product.stock} items available'
                )
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return self.cart_response(
                True, 
                'Cart updated',
                item_total=str(cart_item.get_total_price())
            )
        
        except CartItem.DoesNotExist:
            return self.cart_response(False, 'Item not found')
        except Exception as e:
            return self.cart_response(False, str(e))


class ClearCartView(CartActionView):
    """Clear all items from cart.
    
    AJAX endpoint that removes all cart items.
    Returns JSON with success status.
    """

    def post(self, request, *args, **kwargs):
        """Handle clear cart request.
        
        Removes all items from cart.
        
        Args:
            request: HTTP request
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            JsonResponse with success status
        """
        try:
            cart = self.get_cart()
            cart.items.all().delete()
            return self.cart_response(True, 'Cart cleared')
        except Exception as e:
            return self.cart_response(False, str(e))


# ===== Checkout Views =====

class CheckoutView(LoginRequiredMixin, TemplateView):
    """Display checkout page.
    
    GET: Show checkout form with cart items and shipping options
    POST: Handle shipping method selection (AJAX)
    
    Requires authentication and non-empty cart.
    """
    template_name = 'orders/cart/checkout.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        """Get context data for checkout view.
        
        Includes cart items, totals, shipping info, and customer data.
        
        Returns:
            Context dictionary with checkout information
        """
        context = super().get_context_data(**kwargs)
        
        try:
            cart = Cart.objects.get(user=self.request.user)
            shipping_cost = self._get_shipping_cost()
            
            context.update({
                'cart': cart,
                'cart_items': cart.items.select_related('product'),
                'total_price': cart.get_total_price(),
                'shipping_cost': shipping_cost,
                'grand_total': cart.get_total_price() + shipping_cost,
                'customer': self._get_or_create_customer()
            })
        except Cart.DoesNotExist:
            context['empty_cart'] = True
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle shipping method selection (AJAX).
        
        Stores selected shipping method and cost in session.
        
        Args:
            request: HTTP request with POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            JsonResponse with success status
        """
        try:
            shipping_method = request.POST.get('shipping_method')
            shipping_cost = request.POST.get('shipping_cost')
            
            # Store in session
            request.session['shipping_method'] = shipping_method
            request.session['shipping_cost'] = shipping_cost
            request.session.modified = True
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error setting shipping'
            }, status=500)
    
    def _get_shipping_cost(self):
        """Helper to get shipping cost from session.
        
        Returns:
            Decimal shipping cost from session or default 10.00
        """
        try:
            return Decimal(self.request.session.get('shipping_cost', '10.00'))
        except Exception:
            return Decimal('10.00')
    
    def _get_or_create_customer(self):
        """Helper to get or create customer for current user.
        
        Returns:
            Customer instance for current user
        """
        customer, _ = Customer.objects.get_or_create(user=self.request.user)
        return customer


class PlaceOrderView(LoginRequiredMixin, View):
    """Process checkout and create order.
    
    POST only: Creates order from cart items, updates customer info,
    clears cart, and redirects to confirmation page.
    
    Validates non-empty cart before processing.
    """
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        """Process checkout and create order.
        
        Creates order from cart items, updates customer info,
        clears cart, and redirects to confirmation page.
        
        Args:
            request: HTTP request with POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            Redirect to order confirmation page or back to checkout
        """
        try:
            cart = Cart.objects.get(user=request.user)
            
            if not cart.items.exists():
                messages.error(request, 'Your cart is empty')
                return redirect('orders:cart')
            
            # Get or create customer
            customer, _ = Customer.objects.get_or_create(user=request.user)
            
            # Update customer info
            customer.phone = request.POST.get('phone', customer.phone)
            customer.address = request.POST.get('address', customer.address)
            customer.save()
            
            # Calculate total
            shipping_cost = self._get_shipping_cost()
            total = cart.get_total_price() + shipping_cost
            
            # Create order
            order = Order.objects.create(
                customer=customer,
                total_price=total,
                status='N',
                address=request.POST.get('address', customer.address) or 'Not provided',
                is_draft=False
            )
            
            # Add order items
            for cart_item in cart.items.all():
                OrderElement.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('orders:order_confirmation', order_uuid=order.uuid)
        
        except Cart.DoesNotExist:
            messages.error(request, 'Your cart is empty')
            return redirect('orders:cart')
        except Exception as e:
            logging.getLogger(__name__).error(f'Order error: {e}', exc_info=True)
            messages.error(request, 'An error occurred while placing order')
            return redirect('orders:checkout')
    
    def _get_shipping_cost(self):
        """Helper to get shipping cost from session.
        
        Returns:
            Decimal shipping cost from session or default 10.00
        """
        try:
            return Decimal(self.request.session.get('shipping_cost', '10.00'))
        except Exception:
            return Decimal('10.00')


class OrderConfirmationView(LoginRequiredMixin, DetailView):
    """Display order confirmation page.
    
    Shows order details including items, total, and shipping info.
    Only allows viewing own orders.
    """
    template_name = 'orders/order_confirmation.html'
    context_object_name = 'order'
    login_url = 'users:login'

    def get_queryset(self):
        """Get orders for current user.
        
        Returns:
            QuerySet of Order objects for current user
        """
        return Order.objects.filter(customer__user=self.request.user)
    
    def get_object(self, queryset=None):
        """Get specific order by UUID.
        
        Args:
            queryset: Optional QuerySet to filter (default: uses get_queryset)
            
        Returns:
            Order instance
        """
        if queryset is None:
            queryset = self.get_queryset()
        order_uuid = self.kwargs.get('order_uuid')
        return get_object_or_404(queryset, uuid=order_uuid)

    def get_context_data(self, **kwargs):
        """Get context data for order confirmation view.
        
        Returns:
            Context dictionary with order and items info
        """
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.get_object().order_items.all()
        context['shipping_cost'] = Decimal('10.00')
        return context


# ===== Order List View =====

class OrderListView(LoginRequiredMixin, TemplateView):
    """Display all user orders.
    
    Shows list of orders for authenticated user, excluding drafts.
    """
    template_name = 'orders/order_list.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        """Get context data for order list view.
        
        Returns:
            Context dictionary with user's orders
        """
        context = super().get_context_data(**kwargs)
        try:
            customer = self.request.user.customer
            context['orders'] = Order.objects.filter(
                customer=customer,
                is_draft=False
            ).order_by('-registered_at')
        except Exception:
            context['orders'] = []
        
        return context
