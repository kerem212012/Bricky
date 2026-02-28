"""Custom Django template filters for core app.

Provides custom filters for:
- Mathematical operations in templates
- String formatting
"""
from django import template

register = template.Library()

@register.filter
def mul(value, arg):

    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):

    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
