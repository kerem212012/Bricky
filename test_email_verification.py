#!/usr/bin/env python
"""
Test script to verify email token generation and validation
Run with: python manage.py shell < test_email_verification.py
Or: python manage.py shell -c "exec(open('test_email_verification.py').read())"
"""

import os
import sys
import django
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.models import CustomUser

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

User = get_user_model()

# Test token generation and validation
print("=" * 60)
print("EMAIL VERIFICATION TOKEN TEST")
print("=" * 60)

# Get or create a test user
try:
    user = User.objects.get(username='testuser')
    print(f"\nUsing existing test user: {user.username} (ID: {user.pk})")
except User.DoesNotExist:
    print("\nCreating test user...")
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print(f"Created test user: {user.username} (ID: {user.pk})")

# Refresh to ensure password hash is set
user.refresh_from_db()
print(f"User password hash: {user.password[:30]}...")
print(f"User PK: {user.pk}")

# Generate token
print("\n" + "-" * 60)
print("TOKEN GENERATION")
print("-" * 60)
token = default_token_generator.make_token(user)
print(f"Generated token: {token[:50]}...")
print(f"Token length: {len(token)}")

# Encode UID
uid = urlsafe_base64_encode(force_bytes(user.pk))
print(f"Encoded UID: {uid}")

# Decode and verify UID
decoded_uid = urlsafe_base64_decode(uid).decode()
print(f"Decoded UID: {decoded_uid}")
print(f"UID matches user.pk: {int(decoded_uid) == user.pk}")

# Validate token
print("\n" + "-" * 60)
print("TOKEN VALIDATION")
print("-" * 60)

# Refresh user from DB (simulating what happens when validating from a link)
user.refresh_from_db()
is_valid = default_token_generator.check_token(user, token)
print(f"Token is valid: {is_valid}")

if not is_valid:
    print("\nDEBUGGING TOKEN FAILURE:")
    print(f"  - User password hash: {user.password}")
    print(f"  - Token (first 100 chars): {token[:100]}")
    
    # Try to create a new token and validate it immediately
    print("\nTrying immediate validation...")
    token2 = default_token_generator.make_token(user)
    is_valid2 = default_token_generator.check_token(user, token2)
    print(f"Immediate token validation: {is_valid2}")
    
    if not is_valid2:
        print("\nERROR: Even immediate token validation failed!")
        print("This suggests a Django configuration or token settings issue.")
else:
    print("\n✓ Token validation successful!")
    print("\nYour email verification system should work correctly.")

print("\n" + "=" * 60)
