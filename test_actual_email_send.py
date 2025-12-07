#!/usr/bin/env python
import os
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from users.views import send_verification

User = get_user_model()

# Create a new test user
try:
    test_user = User.objects.get(username='test_email_send')
    test_user.delete()
except User.DoesNotExist:
    pass

test_user = User.objects.create_user(
    username='test_email_send',
    email='test_send@example.com',
    password='testpass123'
)

print("=" * 70)
print("TESTING ACTUAL EMAIL SENDING")
print("=" * 70)

print(f"\nCreated test user: {test_user.username}")
print(f"Email: {test_user.email}")

# Create a fake request
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'

print("\n" + "-" * 70)
print("SENDING VERIFICATION EMAIL")
print("-" * 70)

# Send verification email
send_verification(request, test_user)

print("\n" + "=" * 70)
print("Check your email backend output above for the URL")
print("=" * 70)
