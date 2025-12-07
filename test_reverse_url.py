#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from django.urls import reverse

# Test what reverse generates
link = reverse("users:verify_email", kwargs={"uidb64": "test123", "token": "testtoken"})
print(f"reverse('users:verify_email') generates: {link}")

# This is correct - it should include 'users/' because of how the URLs are configured
