import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional
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
    user: CustomUser = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    phone: Optional[str] = PhoneNumberField(blank=True)
    address: Optional[str] = models.TextField(max_length=500,blank=True)

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
        BILLED = "P", "Billed order"
        PROCESSED = "P", "Processed"
        SHIPPED = "S", "Shipped order"
        COMPLETED = "C", "Completed order"
        DROPPED = "D", "Dropped order"

    status: str = models.CharField(max_length=1, choices=StatusChoice.choices, db_index=True,
                              default=StatusChoice.NEW)
    customer:Customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address: Optional[str] = models.TextField(blank=True)
    is_draft: bool = models.BooleanField(default=True)
    order_note: Optional[str] = models.TextField(max_length=200, blank=True)
    registered_at: datetime = models.DateTimeField(default=timezone.now)
    called_at: Optional[datetime] = models.DateTimeField(db_index=True, blank=True, null=True)
    delivered_at: Optional[datetime] = models.DateTimeField(db_index=True, blank=True, null=True)
    total_price: Decimal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} | {self.status}"

    def calculate_total(self):
        total = sum(item.total_price for item in self.order_items.all())
        self.total_price = total
        self.save(update_fields=["total_price"])
        return total

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'



class OrderElement(models.Model):
    """
    Model representing an item in an order
    """
    order: Order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
    )
    product: Optional[Product] = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="order_elements"
    )
    price: Decimal  = models.DecimalField(max_digits=8, decimal_places=2)
    quantity: int = models.PositiveIntegerField(default=1)

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Order Element'
        verbose_name_plural = 'Order Elements'
