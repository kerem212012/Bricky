"""ASGI config for Bricky LEGO store project.

Exposes the ASGI callable for asynchronous web servers.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')

application = get_asgi_application()
