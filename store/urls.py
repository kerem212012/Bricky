from django.urls import path

from store import views

app_name = "store"

urlpatterns = [
    path('', views.LegoStoreView.as_view(), name='lego_store'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]