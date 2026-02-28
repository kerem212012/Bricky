"""Django app configuration for core app.

Handles general site functionality, contact messages, and help articles.
"""

from django.apps import AppConfig

class CoreConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
