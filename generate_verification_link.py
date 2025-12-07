#!/usr/bin/env python
"""
Generate a valid email verification link for a user.

Usage:
    python manage.py shell
    >>> exec(open('generate_verification_link.py').read())
    >>> generate_link('username')
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


def generate_link(username):
    """Generate a valid verification link for a user."""
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"✗ User '{username}' not found")
        return None
    
    if user.email_is_verified:
        print(f"ℹ User '{username}' email is already verified")
        return None
    
    try:
        # Generate token from fresh database fetch
        user = User.objects.get(pk=user.pk)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        if isinstance(uid, bytes):
            uid = uid.decode()
        
        # Validate token
        is_valid = default_token_generator.check_token(user, token)
        
        if not is_valid:
            print(f"✗ Token generation failed for user '{username}'")
            return None
        
        link = f"http://127.0.0.1:8000/users/verify-email/{uid}/{token}/"
        
        print(f"✓ Verification link generated for user '{username}':")
        print(f"\n  User: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Link: {link}")
        print("\nCopy and paste this link into your browser to verify the email.")
        
        return link
        
    except Exception as e:
        print(f"✗ Error generating link: {str(e)}")
        return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        username = sys.argv[1]
        generate_link(username)
    else:
        print("Usage: generate_link('username')")
