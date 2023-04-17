from django.db import models
from Product.models import Products
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class ShipTracker(models.Model):
    STATUS_CHOICES = (
    ('created','Created'),('shipped','Shipped'),('delivered','delivered'),('refunded','refunded')
)  
    
    carrier_name = models.CharField(max_length=20, null=True,blank=True)
    carrier_code = models.CharField(max_length=10, null=True, blank=True)
    tracking_number = models.CharField(max_length=50,null=True,blank=True)
    eventId = models.CharField(max_length=20, null=True, blank=True)
    order_ship = models.ForeignKey(Products,on_delete=models.CASCADE, related_name="product_shipping")
    shipping_time = models.DateField( _("Shipping Time"), blank=True, null=True)    
    order_status_description = models.CharField(max_length=20, null=True,blank=True)    
    sender_shipping = models.ForeignKey(User,related_name="seller_product",on_delete=models.CASCADE)
    recipient_shipping = models.ForeignKey(User, related_name="buyer_product",on_delete=models.CASCADE)
    order_created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateField(null=True,blank=True)    
    recipient_address = models.CharField(max_length=50, null=True, blank=True)
    sender_address = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(null=False, max_length=15)
    updated_at = models.DateField(null=True,blank=True)
    comment = models.CharField(null=True, blank=True, max_length=30)
    destination_country = models.CharField(max_length=20)
    state = models.CharField(max_length=20, null=True, blank=True)    
    city = models.CharField(max_length=20)
    appartment = models.CharField(max_length=20)      
    district = models.CharField(max_length=20,null=True, blank=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="created", max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    email = models.EmailField()
    
    
    
    
    def __str__(self):
        return str(self.order_ship)
    
    


