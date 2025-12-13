from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('new-releases/', views.NewReleasesView.as_view(), name='new_releases'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Newsletter URLs
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/subscribe-ajax/', views.NewsletterSubscribeAjaxView.as_view(), name='newsletter_subscribe_ajax'),
    path('newsletter/success/', views.NewsletterSuccessView.as_view(), name='newsletter_success'),
    
    # Cart & Checkout URLs
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/remove/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/update/', views.UpdateCartItemView.as_view(), name='update_cart'),
    path('cart/clear/', views.ClearCartView.as_view(), name='clear_cart'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/place/', views.PlaceOrderView.as_view(), name='place_order'),
    path('order/<uuid:order_id>/confirmation/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
    
    # API URLs
    path('api/search/', views.search_api, name='search_api'),
    path('api/autocomplete/', views.search_autocomplete, name='search_autocomplete'),
    
    # Review URLs
    path('review/create/', views.CreateReviewView.as_view(), name='create_review'),
    path('review/<uuid:review_id>/helpful/', views.ReviewHelpfulView.as_view(), name='review_helpful'),
]