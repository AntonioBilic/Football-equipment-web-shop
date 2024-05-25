from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from  phonenumber_field.modelfields import PhoneNumberField


STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),

)

RATING = (
    ( 1, "★☆☆☆☆"), 
    ( 2, "★★☆☆☆"),
    ( 3, "★★★☆☆"),
    ( 4, "★★★★☆"),
    ( 5, "★★★★★"),
)


class User(AbstractUser):
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   email = models.EmailField()
   phone_number = PhoneNumberField()
   address = models.TextField()



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField() #for user friendly-urls


    class Meta:
        ordering = ('name',) # order in alphabet order
    


    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=12, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField()
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    #old price specification, tags
    
    

    
    def __str__(self):
        return self.name

    #def product_image(self):
        
    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField()
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE) 

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_staus = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")




class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE )
    item = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)



class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review =  models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.name
    
    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date =  models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return self.product.name
     