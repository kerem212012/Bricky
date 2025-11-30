from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decimal import Decimal
from datetime import timedelta
import json

from users.models import CustomUser
from orders.models import Order, Customer, OrderElement
from store.models import Product, Category, Cart, CartItem


class CategoryView(ListView):
    """
    Category detail page showing all products for a specific category with filtering
    """
    model = Product
    template_name = 'core/category.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        category_slug = self.kwargs.get('slug')
        queryset = Product.objects.filter(
            category__slug=category_slug, 
            is_active=True
        ).select_related('category')
        
        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Stock availability filter
        in_stock = self.request.GET.get('in_stock')
        if in_stock == 'true':
            queryset = queryset.filter(stock__gt=0)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('slug')
        category = Category.objects.get(slug=category_slug)
        
        # Get filter values
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        in_stock = self.request.GET.get('in_stock', '')
        sort = self.request.GET.get('sort', '-created_at')
        
        # Get products for stats
        all_products = Product.objects.filter(category__slug=category_slug, is_active=True)
        
        context['category'] = category
        context['min_price'] = min_price
        context['max_price'] = max_price
        context['in_stock'] = in_stock
        context['sort'] = sort
        context['products_count'] = all_products.count()
        context['other_categories'] = Category.objects.exclude(slug=category_slug)[:6]
        
        # Get min price for stats
        if all_products.exists():
            context['min_price_stat'] = all_products.order_by('price').first().price
        else:
            context['min_price_stat'] = 0
        
        return context


class IndexView(ListView):
    
    """
    LEGO store main page showing all products with filters and categories
    """
    model = Product
    template_name = 'core/index.html'
    context_object_name = 'object_list'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['sort'] = self.request.GET.get('sort', '-created_at')
        
        # Price range for filter
        products = Product.objects.filter(is_active=True)
        if products.exists():
            context['price_max'] = products.order_by('-price').first().price
            context['price_min'] = products.order_by('price').first().price
        
        return context


class ShopView(ListView):
    """
    Dedicated shop page with advanced filtering and sorting
    """
    model = Product
    template_name = 'core/shop.html'
    context_object_name = 'object_list'
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Category filter
        categories = self.request.GET.getlist('category')
        if categories:
            queryset = queryset.filter(category__slug__in=categories)
        
        # Price filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Availability filter
        availability = self.request.GET.get('availability')
        if availability == 'in_stock':
            queryset = queryset.filter(stock__gt=0)
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'price-low':
            queryset = queryset.order_by('price')
        elif sort == 'price-high':
            queryset = queryset.order_by('-price')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        elif sort == 'popular':
            queryset = queryset.order_by('-stock')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_categories'] = self.request.GET.getlist('category')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        
        return context


class ProductDetailView(DetailView):
    """
    View for displaying a single product's details
    """
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class PrivacyPolicyView(TemplateView):
    """
    View for displaying the Privacy Policy page
    """
    template_name = 'core/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    """
    View for displaying the Terms of Service page
    """
    template_name = 'core/terms_of_service.html'


class CookieSettingsView(TemplateView):
    """
    View for displaying the Cookie Settings page
    """
    template_name = 'core/cookie_settings.html'


class AboutView(TemplateView):
    """
    View for displaying the About page
    """
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """
    View for displaying the Contact page
    """
    template_name = 'core/contact.html'


class NewReleasesView(TemplateView):
    """
    View for displaying the New Releases page with old and coming soon products
    """
    template_name = 'core/new_releases.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get status filter from query params
        status = self.request.GET.get('status', '')
        
        # Get sorting from query params
        sort = self.request.GET.get('sort', '-created_at')
        
        # Base queryset for active products with NEW, OLD or COMING_SOON status
        queryset = Product.objects.filter(
            is_active=True,
            status__in=['N', 'O', 'C']  # New, Old and Coming Soon products
        ).select_related('category')
        
        # Apply status filter if provided
        if status == 'new':
            queryset = queryset.filter(status='N')
        elif status == 'old':
            queryset = queryset.filter(status='O')
        elif status == 'coming_soon':
            queryset = queryset.filter(status='C')
        
        # Apply sorting
        queryset = queryset.order_by(sort)
        
        # Separate products by status
        new_products = Product.objects.filter(
            is_active=True,
            status='N'
        ).select_related('category').order_by(sort)
        
        old_products = Product.objects.filter(
            is_active=True,
            status='O'
        ).select_related('category').order_by(sort)
        
        coming_soon_products = Product.objects.filter(
            is_active=True,
            status='C'
        ).select_related('category').order_by(sort)
        
        context['products'] = queryset
        context['new_products'] = new_products
        context['old_products'] = old_products
        context['coming_soon_products'] = coming_soon_products
        context['status_filter'] = status
        context['sort'] = sort
        context['categories'] = Category.objects.all()
        
        return context


class SearchView(ListView):
    """
    Comprehensive search view for products and categories
    """
    model = Product
    template_name = 'core/search.html'
    context_object_name = 'results'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return Product.objects.none()
        
        # Search in products
        queryset = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__title__icontains=query),
            is_active=True
        ).select_related('category').distinct()
        
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        
        context['search_query'] = query
        context['query_length'] = len(query)
        
        # Get search statistics
        if query and len(query) >= 2:
            products = self.get_queryset()
            categories = Category.objects.filter(title__icontains=query)
            
            context['total_results'] = products.count()
            context['categories'] = categories
            context['search_performed'] = True
        else:
            context['search_performed'] = False
        
        return context


def search_api(request):
    """
    API endpoint for instant search suggestions
    """
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'results': []})
    
    # Search products
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_active=True
    ).values('id', 'name', 'slug', 'price')[:5]
    
    # Search categories
    categories = Category.objects.filter(
        title__icontains=query
    ).values('id', 'title', 'slug')[:3]
    
    results = {
        'products': list(products),
        'categories': list(categories),
    }
    
    return JsonResponse(results)


def search_autocomplete(request):
    """
    Autocomplete suggestions for search bar
    """
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 1:
        return JsonResponse({'suggestions': []})
    
    # Get product names
    products = Product.objects.filter(
        name__icontains=query,
        is_active=True
    ).values_list('name', flat=True).distinct()[:10]
    
    # Get category names
    categories = Category.objects.filter(
        title__icontains=query
    ).values_list('title', flat=True).distinct()[:5]
    
    suggestions = {
        'products': list(products),
        'categories': list(categories),
    }
    
    return JsonResponse(suggestions)


# ============ CART VIEWS ============

class CartView(LoginRequiredMixin, TemplateView):
    """
    Display user's shopping cart with all items
    """
    template_name = 'core/cart.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        
        context['cart'] = cart
        context['cart_items'] = cart.items.all().select_related('product')
        context['total_price'] = cart.get_total_price()
        context['total_items'] = cart.get_total_items()
        context['shipping_cost'] = Decimal('10.00') if cart.get_total_items() > 0 else Decimal('0')
        context['tax'] = (context['total_price'] * Decimal('0.1')).quantize(Decimal('0.01'))
        context['grand_total'] = context['total_price'] + context['shipping_cost'] + context['tax']
        
        return context


class AddToCartView(LoginRequiredMixin, View):
    """
    Add a product to the user's cart (AJAX endpoint)
    """
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            # Validate stock
            if product.stock < quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Only {product.stock} items available in stock'
                }, status=400)
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Add or update cart item
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                # Item already in cart, update quantity
                cart_item.quantity += quantity
                cart_item.save()
                item_created = False
            except CartItem.DoesNotExist:
                # Create new cart item
                cart_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    price=product.price,
                    quantity=quantity
                )
                item_created = True
            
            return JsonResponse({
                'success': True,
                'message': f'{product.name} added to cart',
                'cart_count': cart.get_total_items(),
                'cart_total': str(cart.get_total_price())
            })
        
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            }, status=404)


class RemoveFromCartView(LoginRequiredMixin, View):
    """
    Remove an item from the cart
    """
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cart_item_id')
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            cart = cart_item.cart
            product_name = cart_item.product.name
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'{product_name} removed from cart',
                'cart_count': cart.get_total_items(),
                'cart_total': str(cart.get_total_price())
            })
        
        except CartItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not found in cart'
            }, status=404)


class UpdateCartItemView(LoginRequiredMixin, View):
    """
    Update quantity of an item in the cart
    """
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
            
            # Validate quantity
            if quantity < 1:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'message': 'Item removed from cart'
                })
            
            # Validate stock
            if cart_item.product.stock < quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Only {cart_item.product.stock} items available in stock'
                }, status=400)
            
            cart_item.quantity = quantity
            cart_item.save()
            cart = cart_item.cart
            
            return JsonResponse({
                'success': True,
                'message': 'Cart updated',
                'item_total': str(cart_item.get_total_price()),
                'cart_count': cart.get_total_items(),
                'cart_total': str(cart.get_total_price())
            })
        
        except CartItem.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Item not found'
            }, status=404)


class ClearCartView(LoginRequiredMixin, View):
    """
    Clear all items from the cart
    """
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Cart cleared',
                'cart_count': 0,
                'cart_total': '0.00'
            })
        
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cart not found'
            }, status=404)


class CheckoutView(LoginRequiredMixin, TemplateView):
    """
    Checkout page with shipping and payment information
    """
    template_name = 'core/checkout.html'
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            cart = Cart.objects.get(user=self.request.user)
            context['cart'] = cart
            context['cart_items'] = cart.items.all().select_related('product')
            context['total_price'] = cart.get_total_price()
            context['shipping_cost'] = Decimal('10.00') if cart.get_total_items() > 0 else Decimal('0')
            context['tax'] = (context['total_price'] * Decimal('0.1')).quantize(Decimal('0.01'))
            context['grand_total'] = context['total_price'] + context['shipping_cost'] + context['tax']
            
            # Get or create customer
            customer, created = Customer.objects.get_or_create(user=self.request.user)
            context['customer'] = customer
            
        except Cart.DoesNotExist:
            context['empty_cart'] = True
        
        return context


class PlaceOrderView(LoginRequiredMixin, View):
    """
    Process the checkout and create an order
    """
    login_url = 'users:login'

    def post(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            
            if not cart.items.exists():
                messages.error(request, 'Your cart is empty')
                return redirect('core:cart')
            
            # Get or create customer
            customer, created = Customer.objects.get_or_create(user=request.user)
            
            # Update customer info from form
            customer.phone = request.POST.get('phone', customer.phone)
            customer.address = request.POST.get('address', customer.address)
            customer.save()
            
            # Create order
            shipping_cost = Decimal('10.00')
            subtotal = cart.get_total_price()
            tax = (subtotal * Decimal('0.1')).quantize(Decimal('0.01'))
            total = subtotal + shipping_cost + tax
            
            order = Order.objects.create(
                customer=customer,
                total_price=total,
                status='N',
                address=request.POST.get('address', customer.address) or 'Not provided'
            )
            
            # Add items to order
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
            return redirect('core:order_confirmation', order_id=order.id)
        
        except Cart.DoesNotExist:
            messages.error(request, 'Cart not found')
            return redirect('core:cart')
        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
            return redirect('core:checkout')


class OrderConfirmationView(LoginRequiredMixin, DetailView):
    """
    Display order confirmation page
    """
    model = Order
    template_name = 'core/order_confirmation.html'
    context_object_name = 'order'
    login_url = 'users:login'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        # Only show orders for the current user
        return Order.objects.filter(customer__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['order_items'] = order.order_items.all()
        context['shipping_cost'] = Decimal('10.00')
        # Calculate tax from total_price (total - shipping = subtotal, subtotal * 0.1 = tax)
        subtotal = order.total_price - Decimal('10.00')
        context['tax'] = (subtotal * Decimal('0.1')).quantize(Decimal('0.01'))
        
        return context

