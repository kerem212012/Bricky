/* Cart Page JavaScript Functions */

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show notification with animation
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const colors = {
        'success': '#4caf50',
        'error': '#f44336',
        'warning': '#ff9800',
        'info': '#2196f3'
    };
    
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        padding: 16px 24px;
        background: ${colors[type] || colors['info']};
        color: white;
        border-radius: 6px;
        z-index: 1000;
        animation: slideUp 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        max-width: 90%;
        max-width: 350px;
        font-weight: 500;
        font-size: 14px;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideDown 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Update cart count in navbar
function updateCartCount(count) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = count;
        cartCount.style.animation = 'pulse 0.4s ease';
        setTimeout(() => {
            cartCount.style.animation = 'none';
        }, 400);
    }
}

// Remove item from cart
function removeFromCart(cartItemId) {
    if (!confirm('Are you sure you want to remove this item from your cart?')) {
        return;
    }

    const itemElement = document.querySelector(`[data-item-id="${cartItemId}"]`);
    if (itemElement) {
        itemElement.style.animation = 'slideDown 0.3s ease forwards';
    }

    const form = new FormData();
    form.append('cart_item_id', cartItemId);

    fetch(window.CART_URLS.remove_from_cart, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            setTimeout(() => {
                if (itemElement) {
                    itemElement.remove();
                }
                updateCartCount(data.cart_count);
                updateCartSummary(data.cart_total);
                showNotification(data.message, 'success');
                
                // Check if cart is now empty
                const cartItems = document.querySelectorAll('.cart-item');
                if (cartItems.length === 0) {
                    location.reload();
                }
            }, 300);
        } else {
            itemElement.style.animation = 'slideIn 0.3s ease';
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        itemElement.style.animation = 'slideIn 0.3s ease';
        showNotification('Error removing item from cart', 'error');
    });
}

// Update quantity
function updateQuantity(cartItemId, newQuantity) {
    const qtyInput = document.querySelector(`[data-item-id="${cartItemId}"] .qty-input`);
    const itemElement = document.querySelector(`[data-item-id="${cartItemId}"]`);
    
    newQuantity = parseInt(newQuantity);
    
    if (isNaN(newQuantity) || newQuantity < 1) {
        removeFromCart(cartItemId);
        return;
    }

    // Add loading state
    itemElement.style.opacity = '0.7';
    itemElement.style.pointerEvents = 'none';

    const form = new FormData();
    form.append('cart_item_id', cartItemId);
    form.append('quantity', newQuantity);

    fetch(window.CART_URLS.update_cart, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update item total
            const itemTotalElement = itemElement.querySelector('.item-total');
            itemTotalElement.textContent = '$' + parseFloat(data.item_total).toFixed(2);
            itemTotalElement.style.animation = 'slideUp 0.3s ease';
            
            // Update cart total
            updateCartSummary(data.cart_total);
            updateCartCount(data.cart_count);
            
            // Remove loading state
            itemElement.style.opacity = '1';
            itemElement.style.pointerEvents = 'auto';
            
            showNotification('Cart updated successfully', 'success');
        } else {
            // Revert quantity
            qtyInput.value = qtyInput.getAttribute('data-original') || 1;
            itemElement.style.opacity = '1';
            itemElement.style.pointerEvents = 'auto';
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        itemElement.style.opacity = '1';
        itemElement.style.pointerEvents = 'auto';
        showNotification('Error updating quantity', 'error');
    });
}

// Update cart summary display
function updateCartSummary(cartTotal) {
    const grandTotalElement = document.querySelector('.grand-total');
    if (grandTotalElement) {
        grandTotalElement.textContent = '$' + parseFloat(cartTotal).toFixed(2);
        grandTotalElement.style.animation = 'pulse 0.4s ease';
    }
}

// Clear entire cart
function clearCart() {
    if (!confirm('Are you sure you want to clear your entire cart? This action cannot be undone.')) {
        return;
    }

    const cartItemsTable = document.querySelector('.cart-items-table');
    if (cartItemsTable) {
        cartItemsTable.style.opacity = '0.7';
        cartItemsTable.style.pointerEvents = 'none';
    }

    const form = new FormData();

    fetch(window.CART_URLS.clear_cart, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Cart cleared successfully', 'success');
            setTimeout(() => {
                location.reload();
            }, 500);
        } else {
            if (cartItemsTable) {
                cartItemsTable.style.opacity = '1';
                cartItemsTable.style.pointerEvents = 'auto';
            }
            showNotification('Error clearing cart', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (cartItemsTable) {
            cartItemsTable.style.opacity = '1';
            cartItemsTable.style.pointerEvents = 'auto';
        }
        showNotification('Error clearing cart', 'error');
    });
}

// Apply promo code
function applyPromo() {
    const promoInput = document.querySelector('.promo-input');
    const promoCode = promoInput.value.trim();
    
    if (!promoCode) {
        showNotification('Please enter a promo code', 'warning');
        return;
    }
    
    showNotification('Promo code "' + promoCode + '" applied! (Feature coming soon)', 'info');
    promoInput.value = '';
}

// Initialize event listeners on page load
document.addEventListener('DOMContentLoaded', function() {
    // Handle clear cart button
    const clearCartBtn = document.getElementById('clear-cart-btn');
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', clearCart);
    }

    // Handle remove button clicks
    document.querySelectorAll('.btn-remove').forEach(btn => {
        btn.addEventListener('click', function() {
            removeFromCart(this.dataset.itemId);
        });
    });

    // Handle quantity decrease buttons
    document.querySelectorAll('.qty-decrease').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.qty-input');
            const newQty = parseInt(input.value) - 1;
            updateQuantity(this.dataset.itemId, newQty);
        });
    });

    // Handle quantity increase buttons
    document.querySelectorAll('.qty-increase').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.qty-input');
            const newQty = parseInt(input.value) + 1;
            updateQuantity(this.dataset.itemId, newQty);
        });
    });

    // Handle quantity input changes
    const qtyInputs = document.querySelectorAll('.qty-input');
    qtyInputs.forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.closest('.cart-item').getAttribute('data-item-id');
            updateQuantity(itemId, this.value);
        });
        
        // Prevent non-numeric input
        input.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    });
    
    // Handle promo button
    const promoBtn = document.getElementById('apply-promo-btn');
    if (promoBtn) {
        promoBtn.addEventListener('click', applyPromo);
        
        // Allow Enter key to apply promo
        const promoInput = document.querySelector('.promo-input');
        if (promoInput) {
            promoInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    applyPromo();
                }
            });
        }
    }
    
    // Add smooth animations to cart items
    const cartItems = document.querySelectorAll('.cart-item');
    cartItems.forEach((item, index) => {
        item.style.animationDelay = (index * 0.1) + 's';
    });
});

// Export functions for inline use
window.removeFromCart = removeFromCart;
window.updateQuantity = updateQuantity;
window.clearCart = clearCart;
window.applyPromo = applyPromo;
window.showNotification = showNotification;
