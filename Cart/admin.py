from django.contrib import admin
from Cart.models import Cart, CartItem

class CartItemAdmin(admin.TabularInline):        
    model = CartItem
    raw_id_fields = ['product']
    


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user","used","created_at"]    
    inlines = [CartItemAdmin]
