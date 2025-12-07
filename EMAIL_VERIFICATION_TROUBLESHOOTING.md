# Email Verification Troubleshooting Guide

## Issue: "Verification Failed - The verification link is invalid or has expired"

This guide helps diagnose and fix email verification issues in the Bricky application.

## System Overview

The email verification system uses Django's built-in `default_token_generator` which:
- Generates tokens based on user password hash and timestamp
- Tokens are valid for 24 hours (configurable via `PASSWORD_RESET_TIMEOUT`)
- Tokens are invalidated if the user's password hash changes

## Common Issues and Solutions

### 1. **Token Generation Timing Issue**
**Problem:** Token generated before user is saved to database

**Solution:** The system now ensures user is saved and refreshed:
```python
if not user.pk:
    user.save()
user.refresh_from_db()
token = default_token_generator.make_token(user)
```

### 2. **Email Not Being Sent**
**Symptoms:** No email received, but no errors shown

**Check:**
- Email backend is configured correctly in settings.py
- Email host credentials are valid in .env
- Check Django console output for email backend messages (in DEBUG mode, emails print to console)

**Debug:**
```bash
python manage.py shell
```
```python
from django.core.mail import send_mail
send_mail('Test', 'Test message', None, ['test@example.com'])
```

### 3. **Token Validation Fails**
**Problem:** Token is invalid even when it should be valid

**Causes:**
- User password changed after token generation
- Token expired (> 24 hours old)
- Server time mismatch between token generation and validation
- User object state inconsistency

**Solution:**
- Refresh user from database before validation: `user.refresh_from_db()`
- Check server time synchronization
- Verify PASSWORD_RESET_TIMEOUT setting

### 4. **Link Format Issues**
**Check URL Structure:**
```
http://127.0.0.1:8000/users/verify-email/{uidb64}/{token}/
```

## Testing Email Verification

### Generate a Valid Verification Link

```bash
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()
user = User.objects.get(username='your_username')

# Ensure fresh state
user.refresh_from_db()

# Generate components
token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
if isinstance(uid, bytes):
    uid = uid.decode()

# Print the URL
print(f"http://127.0.0.1:8000/users/verify-email/{uid}/{token}/")

# Validate token immediately
is_valid = default_token_generator.check_token(user, token)
print(f"Token valid: {is_valid}")
```

### Manual Token Validation

```python
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

User = get_user_model()

# Parse from URL
uidb64 = "NDZmZjI0NGItMGY1NC00YjU4LWE4MmUtOTEzYTRiZWUwYWE3"
token = "d0g7wo-8a971f0e8d1bb5529b5ecf8b20d4d7b5"

try:
    uid = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)
    
    # Check token
    is_valid = default_token_generator.check_token(user, token)
    print(f"Token valid: {is_valid}")
    
except Exception as e:
    print(f"Error: {e}")
```

## Current Implementation

### Files Modified:
1. **users/views.py**
   - `send_verification()`: Enhanced token generation
   - `EmailVerifyView`: Added debugging and refresh_from_db()
   - `ResendVerificationEmailView`: New view for resending emails

2. **users/templates/users/email_verified_failed.html**
   - Added resend email link
   - Shows error message from context

3. **users/templates/users/email_resend.html** (NEW)
   - Dedicated template for resend functionality

4. **bricky/settings.py**
   - Added `PASSWORD_RESET_TIMEOUT = 86400` (24 hours)

## Debug Output

The system now provides detailed logging:
- Email sent successfully: `"Verification email sent successfully to {email}"`
- Token validation: `"Token validation for user {username}: {is_valid}"`
- Email verified: `"Email verified for user {username}"`
- Failures: `"Token validation failed - returning failure page"`

## Features

### Auto-Resend Capability
Users can now resend verification emails at:
```
/users/resend-verification-email/
```

### User-Friendly Error Messages
Failed verification now shows a "Resend Verification Email" button for:
- Authenticated users: Direct link to resend
- Anonymous users: Link to login then resend

## Environment Configuration

Required in .env:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

For Gmail, use an App-Specific Password (not your account password).

## Next Steps if Still Failing

1. Check email backend configuration and credentials
2. Verify database has user saved correctly
3. Check server timezone and time synchronization
4. Review Django logs for email errors
5. Test token generation in Django shell (see above)
6. Check if user password was changed after registration
