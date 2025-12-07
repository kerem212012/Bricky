#!/usr/bin/env python
import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from users.views import send_verification

User = get_user_model()

user = User.objects.get(username='Chipsinka')

print("=" * 70)
print("RESENDING VERIFICATION EMAIL FOR USER")
print("=" * 70)

print(f"\nUser: {user.username}")
print(f"Email: {user.email}")
print(f"Email verified: {user.email_is_verified}")

# Create a fake request
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'

# Send verification email
print("\n" + "-" * 70)
print("SENDING VERIFICATION EMAIL")
print("-" * 70)
send_verification(request, user)

# Generate fresh token and link
print("\n" + "-" * 70)
print("NEW VERIFICATION LINK")
print("-" * 70)

token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
if isinstance(uid, bytes):
    uid = uid.decode()

verify_link = f"http://localhost:8000/users/verify-email/{uid}/{token}/"
print(f"\nFresh verification link:\n{verify_link}")

# Validate the fresh token
is_valid = default_token_generator.check_token(user, token)
print(f"\nToken valid: {is_valid}")

if is_valid:
    print("\n✓ This link should work!")
    print("  Copy and paste the link into your browser")
else:
    print("\n✗ Something went wrong")

print("\n" + "=" * 70)
