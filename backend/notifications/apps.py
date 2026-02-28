"""Django app configuration for notifications app.

Handles newsletter subscription management.
"""

from django.apps import AppConfig

class NotificationsConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
