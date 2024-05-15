
from django.contrib import admin
from django.urls import path,include





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('football_web_shop_app.urls'))
    
]
