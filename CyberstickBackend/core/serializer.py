from dataclasses import field
from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'color', 'price']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'street_address', 'country',
        'zip_code', 'city_state', 'email', 'phone_number']

class OrderSerializer(serializers.ModelSerializer):
    Available = serializers.SerializerMethodField()     
    class Meta:
        model = Order
        fields = ['amount', 'total_price', 'Available']

    def get_Available(self, obj):
        return obj.id

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
          'September', 'October', 'November', 'December']

class SingleOrderSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()    
    date = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    fullname = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'fullname', 'address', 'location', 'email', 'phone',
                  'amount', 'total_price', 'date', 'status']
    
    def get_fullname(self, obj):
        return obj.customer.first_name + ' ' + obj.customer.last_name if obj.customer else None
    
    def get_address(self, obj):
        return obj.customer.street_address if obj.customer else None    
    
    def get_location(self, obj):
        return obj.customer.city_state + ', ' + obj.customer.country if obj.customer else None    

    def get_email(self, obj):
        return obj.customer.email if obj.customer else None

    def get_phone(self, obj):
        return obj.customer.phone_number if obj.customer else None
    
    def get_date(self, obj):
        day = obj.date.day
        month = obj.date.month
        year = obj.date.year
        return f'{months[month-1]} {day:02}, {year}'

class AdminLinkedOrdersSerializer(serializers.Serializer):
    product = serializers.CharField(max_length=1000)
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=11, decimal_places=2)
    total = serializers.DecimalField(max_digits=11, decimal_places=2)