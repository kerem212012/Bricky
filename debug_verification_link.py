#!/usr/bin/env python
import os
import django
from django.test import RequestFactory
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

User = get_user_model()

# The verification link components from user
uidb64 = "MGU1M2YxZGYtODc1NS00MTYzLWE5YzMtNzljYmMxYmYwZDM1"
token = "d0g9b8-1c404ce7f5524825471c40d8a9f413b2"

print("=" * 70)
print("DEBUGGING VERIFICATION LINK")
print("=" * 70)

print(f"\nUID (base64): {uidb64}")
print(f"Token: {token}")

# Try to decode UID
try:
    uid = urlsafe_base64_decode(uidb64).decode()
    print(f"\n✓ UID decoded successfully: {uid}")
    
    # Try to find user
    try:
        user = User.objects.get(pk=uid)
        print(f"✓ User found: {user.username} ({user.email})")
        print(f"  Email verified: {user.email_is_verified}")
        print(f"  Password hash: {user.password[:50]}...")
        
        # Test token validation
        is_valid = default_token_generator.check_token(user, token)
        print(f"\n✓ Token validation result: {is_valid}")
        
        if not is_valid:
            print("\n⚠ Token is INVALID. Possible reasons:")
            print("  1. Token has expired (older than 24 hours)")
            print("  2. User password was changed")
            print("  3. User was deleted and recreated")
            print("  4. Token was generated with different SECRET_KEY")
            
            # Try creating a fresh token to test
            print("\n" + "-" * 70)
            print("GENERATING FRESH TOKEN FOR SAME USER")
            print("-" * 70)
            fresh_token = default_token_generator.make_token(user)
            fresh_valid = default_token_generator.check_token(user, fresh_token)
            print(f"Fresh token valid: {fresh_valid}")
            
            if fresh_valid:
                print(f"\n✓ Fresh verification link would work:")
                print(f"  http://localhost:8000/users/verify-email/{uidb64}/{fresh_token}/")
        else:
            print("\n✓ Token is VALID - verification should succeed")
            
    except User.DoesNotExist:
        print(f"✗ User not found with ID: {uid}")
        print("\nAvailable users:")
        for u in User.objects.all():
            print(f"  - {u.username} (ID: {u.pk})")
        
except Exception as e:
    print(f"✗ Error decoding UID: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
