from django.contrib import admin
from .models import User, Address



class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', ]

admin.site.register(User, UserAdmin)

