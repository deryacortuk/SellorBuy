from django.db import models
from django.contrib.auth.models import User
from Product.models import Products

import logging

logger = logging.getLogger(__name__)

class CustomerWishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wishlist")
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name="product_list")
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        return str(self.product)
    