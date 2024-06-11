from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('category_list/', views.category_list, name ='category_list'),
    path('product/<int:id>/', views.product_detail_view, name='product_detail')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)