import uuid

from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal


class Category(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(blank=True, upload_to="user_pictures", default="user_pictures/default.png")
    title: str= models.CharField(max_length=200,unique=True,db_index=True)
    slug:str= models.SlugField(unique=True,db_index=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["title"])
        ]
class Product(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title:str = models.CharField(
        max_length=50,
        db_index=True,
        unique=True
    )
    picture = models.ImageField()
    description:str = models.TextField(
        blank=True,
        max_length=300,
    )
    price:Decimal = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    slug: str = models.SlugField(unique=True, db_index=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["title"])
        ]

