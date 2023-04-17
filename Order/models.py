from django.db import models
from django.contrib.auth.models import User
from Cart.models import Cart
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from Product.models import Products
from django_countries.fields import CountryField
from django.conf import settings


STATUS_CHOICES = (
    ('created','Created'),('paid','Paid'),('shipped','Shipped'),('delivered','delivered'),('refunded','refunded')
)  



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_user")   
    
    stripe_id = models.CharField(max_length=250, blank=True)
    active = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)        
    status = models.CharField(choices=STATUS_CHOICES, default='created',max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)    
    email = models.EmailField()
    phone_number = PhoneNumberField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    country = CountryField(blank_label="(select country)")
    state = models.CharField(max_length=30, null=True, blank=True)    
    city = models.CharField(max_length=20)
    appartment = models.CharField(max_length=20, null=True,blank=True)    
    address = models.CharField(max_length=30)
    district = models.CharField(max_length=30, null=True, blank=True)
    zip_code = models.CharField(max_length=10)
    
    
    
    class Meta:
        ordering = ('-created_at',)
        
    
    def __str__(self):
        return str(self.id)
    
    def get_total_cost(self):
        return round(sum(item.total() for item in self.items.all()),2)
    
    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '__test__' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f"https://dashoard.stripe.com{path}payments/{self.stripe_id}"
    
 
    


class OrderItem(models.Model):
    order= models.ForeignKey(Order,related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name="order_items",on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    def total(self):
        return round(self.price * self.quantity,2)
