from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)

RATING = (
    (1, "★☆☆☆☆"), 
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField()
    country = CountryField()
    city = models.CharField(max_length=100,null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = CountryField()

    def __str__(self):
        return f"{self.user.username} - {self.address_line_1}, {self.city}, {self.state}, {self.country}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_subcategories(self):
        return self.subcategories.all()

class Brand(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    SIZE_CHOICES = (
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    )
    name = models.CharField(max_length=2, choices=SIZE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE, default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=12, null=True, blank=True)
    material = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    sizes = models.ManyToManyField(Size, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size.name}"




class ProductImages(models.Model):
    images = models.ImageField(upload_to='images/')
    product = models.ForeignKey(Product, related_name='products_image', on_delete=models.CASCADE)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, default=0.00)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="pending")
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=30, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.quantity} units - Total: ${self.total_price}"

    @property
    def total_price(self):
        if self.price is None or self.quantity is None:
            return 0
        return self.quantity * self.price

class ProductReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name if self.product else "No product"
    
    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
