#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from django.urls import reverse, get_resolver

# Test if CartView is accessible
try:
    print("Testing 'core:cart' reverse...")
    result = reverse('core:cart')
    print(f"✓ Success: {result}")
except Exception as e:
    print(f"✗ Error: {e}")

# List all URL patterns
print("\nAll core URL patterns:")
resolver = get_resolver()
for pattern in resolver.url_patterns:
    if 'core' in str(pattern):
        print(f"  {pattern}")
