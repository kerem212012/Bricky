"""Django app configuration for users app.

Handles user authentication, profile management, and registration.
"""

from django.apps import AppConfig

class UsersConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
