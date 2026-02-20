from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser
from .models import Customer

@receiver(post_save, sender=CustomUser)
def create_customer_profile(sender, instance, created, **kwargs):

    if created:
        Customer.objects.get_or_create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_customer_profile(sender, instance, **kwargs):

    if hasattr(instance, 'customer'):
        instance.customer.save()
