from rest_framework import serializers
from rest_framework.fields import Field
from Cart.models import Cart, CartItem
from Product.models import Products
from django.utils.translation import gettext_lazy as _



class CartProductSerializer(serializers.ModelSerializer):
    img_mid_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Products
        fields = ["id","title", "seller","slug","price","quantity","img_mid","img_mid_url"]
        read_only_fields = fields
        
    def get_image_url(self, obj):
        return obj.img_mid.url

class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    
    class Meta:
        model = CartItem
        get_cost = Field(source="get_cost")
        fields = ["id","product","quantity","get_cost"]
        
        
    
        
        
  
        
import json    
        
class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(read_only=True, many=True)
    user = serializers.HiddenField(default =serializers.CurrentUserDefault())
    
    class Meta:
        model = Cart
        total = Field(source='total')               
        total_cart_products = Field(source="total_cart_products")
        fields = ["id","user","total","total_cart_products","products"]
        
    def to_representation(self, instance):
        representation = super(CartSerializer, self).to_representation(instance)
        products = representation.pop("products")
        test = json.dumps(products)              
        
        representation["products"] = json.loads(test)

        return representation
    
 