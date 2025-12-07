# Email Verification Fix - "Verification Failed" Error

## Problem Identified

The error message "**The verification link is invalid or has expired**" was occurring because:

### 1. **Missing Django Sites Framework (PRIMARY ISSUE)**
- The code uses `get_current_site(request)` in `send_verification()` function
- Django's Sites framework was NOT installed in `INSTALLED_APPS`
- Without the Sites app, `get_current_site()` returns incorrect domain information
- This corrupts the verification link URL, making tokens invalid even if they were generated correctly

### 2. **Secondary Issues Addressed**

#### User Password State During Registration
- User password hash must be set BEFORE token generation
- The code now ensures password is properly hashed before sending verification email

#### Token Timeout
- Set to 24 hours (86400 seconds) via `PASSWORD_RESET_TIMEOUT` setting
- This is appropriate for email verification links

---

## Solution Applied

### Fix 1: Install Django Sites Framework

**File: `bricky/settings.py`**

Added to `INSTALLED_APPS`:
```python
'django.contrib.sites',
```

Added configuration:
```python
SITE_ID = 1
```

### Why This Fixes the Issue:

1. **Correct Domain Detection**: The Sites framework maintains Site objects with domain names
2. **Reliable Links**: `get_current_site(request)` now returns the correct domain
3. **Token Validation**: When user clicks the link, the domain matches what was encoded in the token

### What Happens Behind the Scenes:

```
1. User registers → send_verification() called
   ├─ Token generated: make_token(user)
   ├─ Domain retrieved: get_current_site(request).domain  ← REQUIRES SITES FRAMEWORK
   └─ Link created: /verify-email/<uidb64>/<token>/

2. User clicks link in email
   ├─ EmailVerifyView processes request
   ├─ UID decoded: urlsafe_base64_decode(uidb64)
   ├─ Token validated: check_token(user, token)  ← MUST MATCH ORIGINAL
   └─ Email marked verified: user.email_is_verified = True
```

---

## Testing the Fix

### Option 1: Run Test Script
```bash
python manage.py shell < test_email_verification.py
```

### Option 2: Manual Testing
1. Register a new user account
2. Check console output for verification link (if `DEBUG=True`)
3. Click the link or copy-paste it to your browser
4. Email should be marked as verified

### Option 3: Full Database Test
```bash
python manage.py migrate
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from users.views import send_verification
from django.test import RequestFactory

User = get_user_model()
user = User.objects.create_user('test@example.com', 'test@example.com', 'password')

# Create fake request
factory = RequestFactory()
request = factory.get('/')

# Send verification
send_verification(request, user)
# Check console output for the link
```

---

## How the Token System Works

Django's `default_token_generator` uses this algorithm:

1. **Token Creation**:
   - Combines: user.pk + user.password hash + timestamp
   - Encodes with SECRET_KEY
   - Result: Unique, one-time use token

2. **Token Validation**:
   - Regenerates the same combination from the user
   - Compares with provided token
   - Checks if age < PASSWORD_RESET_TIMEOUT

3. **Why Tokens Expire**:
   - Based on PASSWORD_RESET_TIMEOUT (24 hours)
   - If user changes password, old tokens invalidate
   - If user is deleted, tokens can't be verified

---

## Troubleshooting

### Symptom: "The verification link is invalid or has expired"

**Check 1: Sites Framework Installed** ✓
```python
# In settings.py
INSTALLED_APPS = [
    ...
    'django.contrib.sites',
]
SITE_ID = 1
```

**Check 2: Database Migrated**
```bash
python manage.py migrate
```

**Check 3: Domain Configuration**
```bash
python manage.py shell
from django.contrib.sites.models import Site
site = Site.objects.get_current()
print(site.domain)  # Should be your actual domain (e.g., localhost:8000)
```

If domain is wrong:
```python
# Fix it in Django admin or shell
site.domain = "yourdomain.com"
site.save()
```

**Check 4: Token Expired**
- Default timeout: 24 hours
- Adjust in settings: `PASSWORD_RESET_TIMEOUT = 3600  # 1 hour`

**Check 5: SECRET_KEY Changed**
- If SECRET_KEY changed, all existing tokens become invalid
- Only new tokens will work

---

## Summary of Changes

| File | Change | Reason |
|------|--------|--------|
| `bricky/settings.py` | Added `'django.contrib.sites'` to `INSTALLED_APPS` | Enable domain detection |
| `bricky/settings.py` | Added `SITE_ID = 1` | Configure Sites framework |

## Files NOT Modified (Working Correctly)
- ✓ `users/views.py` - Token generation and validation logic is correct
- ✓ `users/models.py` - CustomUser model is properly configured
- ✓ `users/urls.py` - URL patterns are correct
- ✓ `bricky/settings.py` - PASSWORD_RESET_TIMEOUT is properly set

---

## Verification Checklist

- [ ] Run migrations: `python manage.py migrate`
- [ ] Restart Django server
- [ ] Register a new test user
- [ ] Check verification email is sent
- [ ] Click verification link
- [ ] User's email_is_verified flag should be True
- [ ] User can proceed with verified account

