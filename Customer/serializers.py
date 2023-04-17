from rest_framework import serializers
from .models import CustomerWishList
from Product.models import Products

class WishlistProductSerializer(serializers.ModelSerializer):
    img_mid_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Products
        fields = ["id","title", "seller","slug","price","quantity","img_mid","img_mid_url"]
        read_only_fields = fields
        
    def get_image_url(self, obj):
        return obj.img_mid.url

class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default =serializers.CurrentUserDefault()) 
    product = WishlistProductSerializer()  
    class Meta:
        model=CustomerWishList
        fields = ["id","user","product","created_at"]    
          
        
        
        