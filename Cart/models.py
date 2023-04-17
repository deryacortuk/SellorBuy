from django.db import models
import logging
from django.contrib.auth.models import User
from Product.models import Products

class CartManager(models.Manager):
    def get_existing_or_new(self, request):
        created = False
        cart_id = request.session.get('cart_id')
        
        if self.get_queryset().filter(id=cart_id, used=False).count==1:
            obj = self.model.objects.get(id=cart_id)
        elif self.get_queryset().filter(user=request.user,used=False).count()==1:
            obj = self.model.objects.get(user=request.user,used=False)
            request.session['cart_id'] =obj.id 
        else:
            obj = self.model.objects.create(user=request.user)
            request.session['cart_id'] = obj.id 
            created = True
        return obj, created
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CartManager()
    
    @property
    def get_products(self):
        return self.products.all()       
        
    
    @property
    def total(self):
        total = 0
        for item in self.products.all():
            total += int(item.quantity)* float(item.product.price)
        return total
    @property
    def tax_total(self):
        total = 0
        for item in self.products.all():
            total += int(item.quantity) * float(item.product.price)* float(item.product.tax)/100
        return total
    @property
    def total_cart_products(self):
        return sum(item.quantity for item in self.products.all())
    
        
    
    
class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="products")
    
    class Meta:
        unique_together = (('product','cart'))
        
    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return round(float(self.product.price) * int(self.quantity),2)
        
    

