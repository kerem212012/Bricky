/* Cart Page JavaScript Functions */

// Store cart operation URLs for cart.js
const addToCartUrl = "{% url 'core:add_to_cart' %}";
const removeFromCartUrl = "{% url 'core:remove_from_cart' %}";
const updateCartUrl = "{% url 'core:update_cart' %}";
const clearCartUrl = "{% url 'core:clear_cart' %}";

function addToCart(productId, quantity = 1) {
    const form = new FormData();
    form.append('product_id', productId);
    form.append('quantity', quantity);

    fetch(addToCartUrl, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            updateCartCount(data.cart_count);
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding to cart', 'error');
    });
}

function removeFromCart(cartItemId) {
    if (!confirm('Remove this item from cart?')) return;

    const form = new FormData();
    form.append('cart_item_id', cartItemId);

    fetch(removeFromCartUrl, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector(`[data-item-id="${cartItemId}"]`).remove();
            updateCartCount(data.cart_count);
            location.reload();
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error removing item', 'error');
    });
}

function updateQuantity(cartItemId, newQuantity) {
    if (newQuantity < 1) {
        removeFromCart(cartItemId);
        return;
    }

    const form = new FormData();
    form.append('cart_item_id', cartItemId);
    form.append('quantity', newQuantity);

    fetch(updateCartUrl, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`[data-item-id="${cartItemId}"]`);
            item.querySelector('.item-total').textContent = '$' + parseFloat(data.item_total).toFixed(2);
            document.querySelector('.grand-total').textContent = '$' + parseFloat(data.cart_total).toFixed(2);
            updateCartCount(data.cart_count);
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error updating quantity', 'error');
    });
}

function clearCart() {
    if (!confirm('Clear all items from cart?')) return;

    const form = new FormData();

    fetch(clearCartUrl, {
        method: 'POST',
        body: form,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error clearing cart', 'error');
    });
}
