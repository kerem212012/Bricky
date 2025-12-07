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

from users.views import send_verification

User = get_user_model()

print("=" * 70)
print("EMAIL VERIFICATION TEST")
print("=" * 70)

# Create test user
try:
    user = User.objects.get(username='verification_test_user')
    print(f"\nUsing existing test user: {user.username}")
    user.delete()
    print("(Deleted old test user)")
except User.DoesNotExist:
    pass

# Create new test user
user = User.objects.create_user(
    username='verification_test_user',
    email='test_verification@example.com',
    password='TestPassword123!'
)
print(f"\n✓ Created test user: {user.username}")
print(f"  Email: {user.email}")
print(f"  Verified: {user.email_is_verified}")

# Create a fake request
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'

# Send verification email
print("\n" + "-" * 70)
print("SENDING VERIFICATION EMAIL")
print("-" * 70)
send_verification(request, user)

# Generate token manually to show the link
print("\n" + "-" * 70)
print("VERIFICATION LINK")
print("-" * 70)

token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
if isinstance(uid, bytes):
    uid = uid.decode()

verify_link = f"http://localhost:8000/verify-email/{uid}/{token}/"
print(f"\nVerification link:\n{verify_link}")

# Test token validation
print("\n" + "-" * 70)
print("TOKEN VALIDATION TEST")
print("-" * 70)

user_from_db = User.objects.get(pk=user.pk)
is_valid = default_token_generator.check_token(user_from_db, token)
print(f"\nToken validation result: {is_valid}")

if is_valid:
    print("✓ Token is VALID - verification should work!")
else:
    print("✗ Token is INVALID - there's a problem with token generation")

print("\n" + "=" * 70)
print("\nTest user credentials:")
print(f"  Username: verification_test_user")
print(f"  Email: test_verification@example.com")
print(f"  Password: TestPassword123!")
print("\nTo verify email manually:")
print(f"  1. Register or login with the test user")
print(f"  2. Visit the verification link above")
print(f"  3. Email should be marked as verified")
print("=" * 70)
