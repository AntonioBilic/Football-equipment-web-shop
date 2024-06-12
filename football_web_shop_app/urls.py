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
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)