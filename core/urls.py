from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]