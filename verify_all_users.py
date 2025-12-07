#!/usr/bin/env python
"""
Verify all users' emails in the database.
Run with: python manage.py shell < verify_all_users.py
"""

from django.contrib.auth import get_user_model

User = get_user_model()

print('='*70)
print('VERIFYING ALL USERS')
print('='*70)

users = User.objects.all()
for user in users:
    print(f"\nUser: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Before: {user.email_is_verified}")
    
    user.email_is_verified = True
    user.save()
    
    # Refresh to confirm
    user = User.objects.get(pk=user.pk)
    print(f"  After: {user.email_is_verified}")

print('\n' + '='*70)
print('FINAL STATUS')
print('='*70)

users = User.objects.all()
for user in users:
    status = '✓ VERIFIED' if user.email_is_verified else '✗ NOT VERIFIED'
    print(f"{user.username:20} | {user.email:35} | {status}")

print('='*70)
