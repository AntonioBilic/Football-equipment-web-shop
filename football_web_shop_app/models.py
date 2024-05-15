from django.db import models


class Product(models.Model):
    category_id = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField()
    

class Order(models.Model):



class OrderItem(models.Model):








class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField() #for user friendly-urls



class Meta:
    ordering = ('name',) # order in alphabet order


def __str__(self):
    return self.name