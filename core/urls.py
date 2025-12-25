from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    
    # Newsletter URLs
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/subscribe-ajax/', views.NewsletterSubscribeAjaxView.as_view(), name='newsletter_subscribe_ajax'),
    path('newsletter/success/', views.NewsletterSuccessView.as_view(), name='newsletter_success'),
]