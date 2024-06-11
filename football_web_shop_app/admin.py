from django.contrib import admin
from .models import User, Address,Product,Wishlist,Order,OrderItem,Category,Size,ProductReview,ProductImages



class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', ]

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['id','name', 'category', 'image', 'price', 'color','material','in_stock','get_sizes']


    def get_sizes(self, obj):
        return ", ".join([size.size for size in obj.sizes.all()])
    get_sizes.short_description = 'Sizes'

class CategoryAdmin(admin.ModelAdmin):
    list_display =['name', 'parent']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','price','paid_status','order_date']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order','item','price','quantity','total']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','country','city','address']

class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'size_type']


    

admin.site.register(User, UserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Size,SizeAdmin)
