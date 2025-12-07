#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from django.contrib.sites.models import Site

site = Site.objects.get_current()
print(f"Current domain: {site.domain}")

# Update to localhost for development
site.domain = "localhost:8000"
site.name = "Bricky Development"
site.save()

print(f"✓ Site updated to: {site.domain}")
