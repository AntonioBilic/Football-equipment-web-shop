from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Product,Wishlist,Order,OrderItem,Category,Size,ProductReview,ProductImages,Brand,ShippingAddress


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['id','name', 'category', 'image', 'price', 'color','material','in_stock','get_sizes']


    def get_sizes(self, obj):
        return ", ".join([size.name for size in obj.sizes.all()])
    get_sizes.short_description = 'Sizes'

class CategoryAdmin(admin.ModelAdmin):
    list_display =['name', 'parent']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'paid_status', 'order_status', 'shipping_address')
    list_filter = ('order_status', 'paid_status', 'order_date')
    search_fields = ('user__username', 'shipping_address__address_line_1', 'shipping_address__city', 'shipping_address__state', 'shipping_address__country')
    inlines = [OrderItemInline]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_1', 'city', 'state', 'postal_code', 'country')
    search_fields = ('user__username', 'address_line_1', 'city', 'state', 'postal_code', 'country')
    

admin.site.register(User, UserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
