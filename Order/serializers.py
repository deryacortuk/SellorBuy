from rest_framework import serializers
from Order.models import Order, OrderItem
from django.utils.translation import gettext_lazy as _



class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ("id","order","product","quantity","price","cost")
        read_only = ("order",)
        
        
    def validate(self, validated_data):
        order_quantity = validated_data["quantity"]
        product_quantity = validated_data["product"].quantity
        product = validated_data["product"]
        order_id = self.context['view'].kwargs.get('order_id')
        
        current_item = OrderItem.objects.filter(product=product,cart__id = order_id)
        if order_quantity > product_quantity:
            error = {'quantity':_('Order quantity is more than the stock.')}
            raise serializers.ValidationError(error)
        if not self.instance and current_item.count() > 0:
            error = {"product":_("Product already exists in your order")}
            raise serializers.ValidationError(error)
        
        return validated_data
    
    def get_price(self,obj):
        return obj.price
    def get_cost(self,obj):
        return obj.cost



class OrderReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.get_full_name",read_only=True)
    order_items = OrderItemSerializer(read_only=True, many=True)
    
    
    class Meta:
        model = Order
        fields = ("id","user","address","payment","order_items","status","paid","created_at","updated_at")
  
