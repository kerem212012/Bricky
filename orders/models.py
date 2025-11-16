import uuid
from decimal import Decimal
from typing import Optional

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from store.models import Product
from users.models import CustomUser


class Customer(models.Model):
    """
    Model representing a customer
    """
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    phone: Optional[str] = PhoneNumberField(blank=True)
    address: str = models.TextField(max_length=500,blank=True)

    def __str__(self) -> str:
        return self.user.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

class Order(models.Model):
    """
    Model representing an order
    """
    class StatusChoice(models.TextChoices):
        NEW = "N", "New order"
        BILLED = "B", "Billed order"
        PROCESSED = "P", "Processed"
        SHIPPED = "S", "Shipped order"
        COMPLETED = "C", "Completed order"
        DROPPED = "D", "Dropped order"

    status = models.CharField(max_length=1, choices=StatusChoice.choices, db_index=True,
                              default=StatusChoice.NEW)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address = models.TextField()
    is_draft = models.BooleanField(default=True)
    order_note = models.TextField(max_length=200, blank=True)
    registered_at = models.DateTimeField(default=timezone.now)
    called_at = models.DateTimeField(db_index=True, blank=True, null=True)
    delivered_at = models.DateTimeField(db_index=True, blank=True, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.user.username} | {self.status}"

    def calculate_total(self):
        total = sum(item.total_price for item in self.order_items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])
        return total


class OrderElement(models.Model):
    """
    Model representing an item in an order
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    product = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="order_elements"
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Order Element'
        verbose_name_plural = 'Order Elements'
