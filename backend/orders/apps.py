"""Django app configuration for orders app.

Handles shopping cart, checkout, and order management.
"""

from django.apps import AppConfig

class OrdersConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    
    def ready(self):

        import orders.signals