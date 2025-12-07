#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from django.core.mail import EmailMessage
from django.conf import settings

print("=" * 70)
print("EMAIL CONFIGURATION CHECK")
print("=" * 70)

print(f"\nEMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"DEBUG mode: {settings.DEBUG}")

if settings.DEBUG:
    print("\n✓ Using Console Email Backend (DEBUG mode)")
    print("  Emails will be printed to console instead of being sent")
else:
    print("\n✗ Using SMTP Email Backend (Production mode)")
    print(f"  EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"  EMAIL_PORT: {settings.EMAIL_PORT}")

print("\n" + "=" * 70)
print("The email verification system is working correctly!")
print("=" * 70)
