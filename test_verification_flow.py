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

from users.views import EmailVerifyView

User = get_user_model()

print("=" * 70)
print("VERIFICATION FLOW TEST - SIMULATING EMAIL CLICK")
print("=" * 70)

# Get the test user
try:
    user = User.objects.get(username='verification_test_user')
    print(f"\n✓ Found test user: {user.username}")
    print(f"  Email verified before: {user.email_is_verified}")
except User.DoesNotExist:
    print("✗ Test user not found. Run test_verification_link.py first.")
    exit(1)

# Generate token and uid
token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
if isinstance(uid, bytes):
    uid = uid.decode()

# Create a fake request and simulate the verification view
factory = RequestFactory()
request = factory.get(f'/verify-email/{uid}/{token}/')
request.META['HTTP_HOST'] = 'localhost:8000'

# Call the EmailVerifyView
view = EmailVerifyView()
view.request = request
view.template_name = 'users/email_verified_success.html'

print("\n" + "-" * 70)
print("SIMULATING EMAIL VERIFICATION CLICK")
print("-" * 70)

response = view.get(request, uidb64=uid, token=token)

# Check if verification was successful
user.refresh_from_db()

print(f"\nResponse status code: {response.status_code}")
print(f"Email verified after: {user.email_is_verified}")

if user.email_is_verified:
    print("\n✓ SUCCESS! Email verification is working correctly!")
    print("  - Token was valid")
    print("  - User email was marked as verified")
else:
    print("\n✗ FAILED! Email was not marked as verified")

print("=" * 70)
