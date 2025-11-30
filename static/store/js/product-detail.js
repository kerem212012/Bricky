/* Product Detail JavaScript Functions */

function changeImage(img) {
    const mainImage = document.getElementById('mainImage');
    mainImage.src = img.src;
    
    document.querySelectorAll('.thumbnail').forEach(thumb => {
        thumb.classList.remove('active');
    });
    img.classList.add('active');
}

function increaseQty(maxStock) {
    const qtyInput = document.getElementById('quantity');
    const current = parseInt(qtyInput.value);
    if (current < maxStock) {
        qtyInput.value = current + 1;
    }
}

function decreaseQty() {
    const qtyInput = document.getElementById('quantity');
    const current = parseInt(qtyInput.value);
    if (current > 1) {
        qtyInput.value = current - 1;
    }
}

function switchTab(e, tabName) {
    e.preventDefault();
    
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName).classList.add('active');
    e.target.classList.add('active');
}

function addToCart(e, productId) {
    e.preventDefault();
    
    const quantity = parseInt(document.getElementById('quantity').value);
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
            document.getElementById('quantity').value = 1;
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding to cart', 'error');
    });
}
