#!/usr/bin/env python
import os
import sys
import json
import django
from django.test import Client
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from store.models import Product, Cart

User = get_user_model()

# Get or create a test user
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()

# Get a product
product = Product.objects.filter(is_active=True).first()
if not product:
    print("ERROR: No active products found")
    sys.exit(1)

print(f"Using product: {product.id} - {product.name}")
print(f"Using user: {user.username}")

# Create a test client and login
client = Client()
client.login(username='testuser', password='testpass123')

# Prepare the data
data = {
    'product_id': str(product.id),
    'quantity': 1
}

print(f"\nSending POST request to /cart/add/ with data: {data}")

# Make the request
response = client.post('/cart/add/', data=data)

print(f"Response Status: {response.status_code}")
print(f"Response Content-Type: {response.get('Content-Type')}")

try:
    response_data = json.loads(response.content)
    print(f"Response Data: {json.dumps(response_data, indent=2)}")
except Exception as e:
    print(f"Could not parse JSON response: {e}")
    print(f"Response Text: {response.content.decode()}")

# Check if cart was created/updated
cart = Cart.objects.filter(user=user).first()
if cart:
    print(f"\nCart found for user {user.username}")
    print(f"Total items: {cart.get_total_items()}")
    print(f"Total price: {cart.get_total_price()}")
    for item in cart.items.all():
        print(f"  - {item.product.name}: {item.quantity}x @ {item.price}")
else:
    print("\nNo cart found for user")
