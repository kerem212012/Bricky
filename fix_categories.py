#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')
django.setup()

from store.models import Category
from django.utils.text import slugify

# Find all categories with empty slugs
empty_slug_categories = Category.objects.filter(slug='')
print(f"Found {empty_slug_categories.count()} categories with empty slugs:")

for category in empty_slug_categories:
    new_slug = slugify(category.title)
    print(f"  - {category.title} → {new_slug}")
    category.slug = new_slug
    category.save()

print("\n✓ All categories fixed!")

# Show all categories
print("\nAll categories:")
for cat in Category.objects.all().order_by('title'):
    print(f"  - {cat.title} (slug: {cat.slug})")
