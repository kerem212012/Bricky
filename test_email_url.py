#!/usr/bin/env python
import os
import re
import django
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

User = get_user_model()

user = User.objects.get(username='kerem')

print("=" * 70)
print("EMAIL URL GENERATION TEST")
print("=" * 70)

# Simulate what happens in send_verification()
factory = RequestFactory()
request = factory.get('/')
request.META['HTTP_HOST'] = 'localhost:8000'

# Generate token and UID
token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
if isinstance(uid, bytes):
    uid = uid.decode()

domain = get_current_site(request).domain
print(f"\n1. Domain from get_current_site(): {domain}")

# Build the verification link
link = reverse("users:verify_email", kwargs={"uidb64": uid, "token": token})
print(f"2. Link from reverse(): {link}")

protocol = "https" if not settings.DEBUG else "http"
verify_url = f"{protocol}://{domain}{link}"
print(f"3. Full verify_url: {verify_url}")

print(f"\n4. DEBUG mode: {settings.DEBUG}")
print(f"5. Protocol used: {protocol}")

# Render the template with this URL
message = render_to_string("users/email_verify.html", {
    "user": user,
    "verify_url": verify_url,
    "domain": domain,
})

print("\n" + "=" * 70)
print("EMAIL CONTENT (first 500 chars):")
print("=" * 70)
print(message[:500])

print("\n" + "=" * 70)
print("VERIFICATION LINK IN EMAIL:")
print("=" * 70)

# Extract the verify_url from the rendered message
urls_in_email = re.findall(r'http[s]?://[^\s<>"{}|\\^`\[\]]*', message)
for url in urls_in_email:
    if 'verify-email' in url:
        print(f"\n✓ Found verification URL: {url}")

print("\n" + "=" * 70)
