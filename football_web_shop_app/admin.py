from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Product, Wishlist, Order, OrderItem, Category, Size, ProductReview,
    ProductImages, Brand, ShippingAddress, ProductSize
)

# Custom User Admin
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Inline for Product Images
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

# Custom Product Admin
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['id', 'name', 'category', 'image', 'price', 'color', 'material', 'in_stock', 'get_sizes']

    def get_sizes(self, obj):
        return ", ".join([size.name for size in obj.sizes.all()])
    get_sizes.short_description = 'Sizes'

# Custom Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']

# Inline for Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'size', 'price', 'quantity', 'total_price')

    def total_price(self, obj):
        if obj.price is None or obj.quantity is None:
            return None
        return obj.price * obj.quantity
    total_price.short_description = 'Total Price'

# Custom Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'price', 'paid_status', 'order_date', 'order_status', 'shipping_address', 'get_order_details')
    list_filter = ('paid_status', 'order_date')
    search_fields = ('user__username', 'payment_id')
    inlines = [OrderItemInline]
    readonly_fields = ('price', 'order_date', 'payment_id')

    def get_order_details(self, obj):
        items = obj.items.all()
        return "; ".join([f"{item.product.name} - Size: {item.size.name} - Qty: {item.quantity} - Price: ${item.price} - Total: ${item.price * item.quantity if item.price is not None and item.quantity is not None else 'N/A'}" for item in items])
    get_order_details.short_description = 'Order Details'

# Custom Order Item Admin
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'get_order_id', 'product', 'size', 'quantity', 'price', 'total_price')
    list_filter = ('order__user', 'product', 'size')
    search_fields = ('product__name', 'order__user__username', 'size__name')

    def get_user(self, obj):
        return obj.order.user.username
    get_user.short_description = 'User'

    def get_order_id(self, obj):
        return obj.order.id
    get_order_id.short_description = 'Order ID'

    def total_price(self, obj):
        if obj.price is None or obj.quantity is None:
            return None
        return obj.price * obj.quantity
    total_price.short_description = 'Total Price'

# Custom Product Review Admin
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

# Custom Product Size Admin
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'stock_quantity']

# Custom Wishlist Admin
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

# Custom Size Admin
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

# Custom Brand Admin
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

# Custom Shipping Address Admin
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line_1', 'city', 'state', 'postal_code', 'country')
    search_fields = ('user__username', 'address_line_1', 'city', 'state', 'postal_code', 'country')

# Registering the models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)
