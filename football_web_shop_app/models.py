from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from  phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField



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


SIZE_TYPE_CHOICES = (
    ('NUM', 'Numerical'),
    ('CAT', 'Categorical'),
)


class User(AbstractUser):
   first_name = models.CharField(max_length=30)
   last_name = models.CharField(max_length=30)
   email = models.EmailField(unique=True)
   phone_number = PhoneNumberField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)  # Ensure unique slugs for each category
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        ordering = ('name',)  # Order categories alphabetically

    def __str__(self):
        return self.name

    def get_subcategories(self):
        return self.subcategories.all()


class Size(models.Model):
    size = models.CharField(max_length=20)
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE_CHOICES)

    def __str__(self):
        return self.size

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=12, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    sizes = models.ManyToManyField(Size, related_name='products')
    #old price specification, tags
    
    

    
    def __str__(self):
        return self.name

 
        
    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, related_name='products_image', on_delete=models.CASCADE) 



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status = models.BooleanField(default=False)
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
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
     
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = CountryField()
    city = models.CharField(max_length=100)
    address = models.TextField() 

    
    def __str__(self):
        return f"{self.address}, {self.city}, {self.country}"