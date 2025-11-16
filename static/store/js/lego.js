/* ============================================
   BRICKY LEGO STORE - Professional JavaScript
   ============================================ */

// Cart Management
let cart = JSON.parse(localStorage.getItem('lego-cart')) || [];

// Update cart count
function updateCartCount() {
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = count;
        cartCount.style.display = count > 0 ? 'flex' : 'none';
    }
}

// Add to cart
function addToCart(productId, productName) {
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            quantity: 1
        });
    }
    
    localStorage.setItem('lego-cart', JSON.stringify(cart));
    updateCartCount();
    showNotification(`${productName} added to bag!`, 'success');
    updateCartDisplay();
}

// Remove from cart
function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    localStorage.setItem('lego-cart', JSON.stringify(cart));
    updateCartCount();
    updateCartDisplay();
}

// Update cart display
function updateCartDisplay() {
    const cartItems = document.getElementById('cart-items');
    if (!cartItems) return;
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Your bag is empty</p>';
        return;
    }
    
    cartItems.innerHTML = cart.map(item => `
        <div class="cart-item" style="padding: 12px; border-bottom: 1px solid #e0e0e0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <strong>${item.name}</strong>
                <button onclick="removeFromCart('${item.id}')" style="background: none; border: none; color: #e40006; cursor: pointer;">×</button>
            </div>
            <div style="display: flex; gap: 8px;">
                <button onclick="decrementQuantity('${item.id}')" style="padding: 4px 8px; border: 1px solid #e0e0e0; background: white; cursor: pointer;">-</button>
                <input type="number" value="${item.quantity}" readonly style="width: 40px; text-align: center; border: 1px solid #e0e0e0;">
                <button onclick="incrementQuantity('${item.id}')" style="padding: 4px 8px; border: 1px solid #e0e0e0; background: white; cursor: pointer;">+</button>
            </div>
        </div>
    `).join('');
}

// Increment quantity
function incrementQuantity(productId) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity += 1;
        localStorage.setItem('lego-cart', JSON.stringify(cart));
        updateCartDisplay();
    }
}

// Decrement quantity
function decrementQuantity(productId) {
    const item = cart.find(item => item.id === productId);
    if (item && item.quantity > 1) {
        item.quantity -= 1;
        localStorage.setItem('lego-cart', JSON.stringify(cart));
        updateCartDisplay();
    }
}

// Toggle cart sidebar
function toggleCart() {
    const sidebar = document.getElementById('cart-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
        updateCartDisplay();
    }
}

// Checkout
function checkout() {
    if (cart.length === 0) {
        showNotification('Your bag is empty', 'warning');
        return;
    }
    showNotification('Proceeding to checkout...', 'info');
    // Redirect to checkout page or payment gateway
    setTimeout(() => {
        console.log('Cart items:', cart);
    }, 1000);
}

// Notify me when back in stock
function notifyMe(productId) {
    showNotification('We\'ll notify you when this item is back in stock!', 'info');
    console.log('Notification request for product:', productId);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : type === 'warning' ? '#ff9800' : '#2196f3'};
        color: white;
        border-radius: 4px;
        z-index: 1000;
        animation: slideUp 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        max-width: 300px;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideDown 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Handle newsletter submission
function handleNewsletter(e) {
    e.preventDefault();
    const email = e.target.querySelector('input[type="email"]').value;
    showNotification(`Thanks! We'll send updates to ${email}`, 'success');
    e.target.reset();
}

// Mobile navigation toggle
function setupMobileNav() {
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
        
        // Close menu when link is clicked
        document.querySelectorAll('.nav-links a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }
}

// Auto-submit filters on change
function setupFilters() {
    const filterForm = document.querySelector('.filter-controls');
    if (!filterForm) return;
    
    filterForm.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', () => {
            // Auto submit on select change
            const applyBtn = filterForm.querySelector('.apply-btn');
            if (applyBtn) {
                applyBtn.click();
            }
        });
    });
}

// Back to top button
function setupBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
}

function backToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();
    updateCartDisplay();
    setupMobileNav();
    setupFilters();
    setupBackToTop();
    
    // Add animations on scroll
    observeElements();
});

// Observe elements for animation
function observeElements() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.product-card, .category-card, .feature').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+C or Cmd+C for cart
    if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
        e.preventDefault();
        toggleCart();
    }
    
    // Ctrl+T or Cmd+T for top
    if ((e.ctrlKey || e.metaKey) && e.key === 't') {
        e.preventDefault();
        backToTop();
    }
});

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideDown {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(20px);
        }
    }
`;
document.head.appendChild(style);
