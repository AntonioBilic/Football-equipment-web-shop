from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_order/<int:product_id>/', views.add_to_order, name='add_to_order'),
    path('order/', views.order_detail, name='order_detail'),
    path('remove_from_order/<int:item_id>/', views.remove_from_order, name='remove_from_order'),
    path('product/<int:id>/', views.product_detail_view, name='product_detail'),
    path('update_order_item_quantity/<int:item_id>/', views.update_order_item_quantity, name='update_order_item_quantity'),
    path('product/<int:product_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('product/<int:product_id>/remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_to_order/<int:product_id>/', views.add_to_order, name='add_to_order'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('settings/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    path('add_shipping_address/', views.add_shipping_address, name='add_shipping_address'),
    path('clear_cart_items/', views.clear_cart_items, name='clear_cart_items'),
  
 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)