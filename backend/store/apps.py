"""Django app configuration for store app.

Handles product catalog, categories, and reviews.
"""

from django.apps import AppConfig

class StoreConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
