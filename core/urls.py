from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('cookie-settings/', views.CookieSettingsView.as_view(), name='cookie_settings'),
]