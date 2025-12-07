#!/usr/bin/env python
import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from users.views import EmailVerifyView

User = get_user_model()

# Get the user
user = User.objects.get(username='Chipsinka')

# Generate fresh token and uid
token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
if isinstance(uid, bytes):
    uid = uid.decode()

print("=" * 70)
print("TESTING FRESH VERIFICATION LINK")
print("=" * 70)

print(f"\nBefore verification:")
print(f"  Username: {user.username}")
print(f"  Email: {user.email}")
print(f"  Email verified: {user.email_is_verified}")

# Simulate clicking the link
factory = RequestFactory()
request = factory.get(f'/users/verify-email/{uid}/{token}/')
request.META['HTTP_HOST'] = 'localhost:8000'

# Call the verification view
view = EmailVerifyView()
response = view.get(request, uidb64=uid, token=token)

# Refresh user from DB
user.refresh_from_db()

print(f"\nAfter verification:")
print(f"  Email verified: {user.email_is_verified}")
print(f"  Response status: {response.status_code}")

if user.email_is_verified:
    print("\n✓ SUCCESS! Email verification worked!")
else:
    print("\n✗ Failed to verify email")

print("\n" + "=" * 70)
