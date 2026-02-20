from django.urls import path
from notifications import views

app_name = "notifications"

urlpatterns = [
    # ===== Newsletter Management =====
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/unsubscribe/', views.NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
]