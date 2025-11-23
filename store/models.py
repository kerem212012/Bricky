import uuid

from django.db import models

class Category(models.Model):
    """
    Model representing a product category
    """
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    picture = models.ImageField(blank=True, upload_to="categories", default="user_pictures/default.png")
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
    name: str = models.CharField(max_length=255, db_index=True)
    slug: str = models.SlugField(unique=True, db_index=True)
    description: str = models.TextField(blank=True)
    picture = models.ImageField(blank=True, upload_to="products", default="products/default.png")
    price: float = models.DecimalField(max_digits=10, decimal_places=2)
    stock: int = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    is_active: bool = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:product_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["is_active"]),
        ]
        ordering = ['-created_at']
