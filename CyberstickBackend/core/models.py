from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from uuid import uuid4

colors = [
    ('black', 'Black'),    
    ('red', 'Red'),
    ('green', 'Green'),
    ('blue', 'Blue'),
]
tags = [
    (1, 'Smart device'),
]
order_statuses = [
    (1, 'not made'),
    (2, 'made'),
    (3, 'pending'),
    (4, 'delivered'),
    (5, 'canceled'),
]
payment_methods = [
    (1, 'card'),
    (2, 'transfer'),
]

phone_regex = RegexValidator(regex=r'^\+?(234)?\d{9,15}$')

def user_directory_path(instance, filename): 
    return 'user_{0}/{1}'.format(instance.id, filename) 
class User(AbstractUser):
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)    
    address = models.CharField('address', max_length=255)
    image = models.ImageField(upload_to=user_directory_path)

def product_image_path(instance, filename): 
    return '{0}_images/{1}'.format(instance.name, filename) 
class Product(models.Model):    
    name = models.CharField('product name', max_length=255, unique=True)
    description = models.TextField('description', null=True)
    tags = models.IntegerField(verbose_name='tags', choices=tags, default=1)
    color = models.CharField(choices=colors, default='black', max_length=5)
    regular_price = models.DecimalField(default=25000.00, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=25000.00, max_digits=10, decimal_places=2)
    weight = models.DecimalField(default=25.00, max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_path, null=True)
    inventory = models.IntegerField(default=1000)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"

    def __str__(self):
        return self.name

class Customer(models.Model):
    first_name = models.CharField('first name', max_length=255)
    last_name = models.CharField('last name', max_length=255)
    street_address = models.CharField('street address', max_length=255)
    country = models.CharField('country', max_length=150)
    zip_code = models.CharField('zip code', max_length=6)
    city_state = models.CharField('city or state', max_length=85)
    email = models.EmailField('email', max_length=255)
    phone_number = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    date = models.DateTimeField('visit date', auto_now_add=True)

    class Meta:
        verbose_name = "Customer"    

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Order(models.Model):
    id = models.UUIDField(verbose_name='serial number', primary_key=True, default=uuid4, editable=False)
    group_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)    
    item = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    amount = models.IntegerField(default=1)
    color = models.CharField(choices=colors, default='black', max_length=5)
    total_price = models.DecimalField('price (ngn)', default=25000.00, max_digits=11, decimal_places=2)
    date = models.DateTimeField('order date', auto_now_add=True)
    status = models.IntegerField('status', choices=order_statuses, default=1)
    payment_method = models.IntegerField('payment method', choices=payment_methods, default=1)

    def __str__(self):
        return 'order ' + str(self.id)
    
    def title(self):
        return 'order for ' + str(self.amount) + ' ' + str(self.item.name)

    def delivery_date(self):
        return self.date + datetime.timedelta(days=10)