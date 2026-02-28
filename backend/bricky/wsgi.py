"""WSGI config for Bricky LEGO store project.

Exposes the WSGI callable for production web servers.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bricky.settings')

application = get_wsgi_application()
