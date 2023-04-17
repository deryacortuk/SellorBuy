from django.shortcuts import redirect, get_object_or_404,render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from Cart.serializers import CartItemSerializer, CartSerializer
from Cart.models import Cart, CartItem
from Product.models import Products
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
import logging
from Product.models import Category
from Order.recommender import Recommender


logger = logging.getLogger(__name__)


    
def cart_quantity(request):
    cartid = int(request.POST.get("cartid"))
    
    cart = Cart.objects.get(id=cartid)
    quantity = int(request.POST.get("quantity"))
    
    id = int(request.POST.get("id"))
    
    product = Products.objects.get(id=id)
    
    cartitem = CartItem.objects.get(cart=cart, product=product)   
    if cartitem.quantity > product.quantity:
        raise ValueError("Quantity exceeded the product quantity")
    cartitem.quantity = quantity
    cartitem.save()
    return JsonResponse(data={"success":"Quantity changed successfully."})
    
    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cart(request,id):
   
    if request.method =="POST":
        product_obj = get_object_or_404(Products, pk=id)
        cart_obj, _ = Cart.objects.get_existing_or_new(request)
        quantity = int(request.data.get("quantity",1)) 
        
        if request.user == product_obj.seller:
            raise PermissionDenied("Adding your own product to your order is not allowed")
        
        if quantity <= 0:
            cart_item_qs = CartItem.objects.filter(cart=cart_obj,product=product_obj)
            if cart_item_qs.count() != 0:
                cart_item_qs.first().delete()
        else:
            cart_item_obj, created = CartItem.objects.get_or_create(product=product_obj,cart=cart_obj)
            cart_item_obj.quantity = quantity
            cart_item_obj.save()
        serializer = CartSerializer(cart_obj, context={"request":request})
        return Response(serializer.data)
        
    

from rest_framework.generics import ListAPIView
import json
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, JsonResponse

class CartListAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "cart/cart.html"
    
    def get(self, request):
        data = Category.objects.all()
        user = request.user        
        cart_list = Cart.objects.filter(user=user, used=False)
        # r = Recommender()
        # cart_products = [item['product'] for item in cart_list.get_products]
        # if cart_products:
        #     recommended_products = r.suggest_products_for(cart_products,max_results=6)
        # else:
        #     recommended_products = []
        
        serializer = CartSerializer(cart_list, context ={"request":request},many=True)
        serializers = json.loads(json.dumps(serializer.data))
        products = serializers[0]["products"]
        total = 0
        id = 0
        
        for con in serializers:
            total = con["total"]    
            id = con["id"]       
       
        return Response({"products":products, "total":total,"id":id,"data":data})
    


@login_required
def delete_product(request,id):
    if request.method == "POST":
        cartitem = CartItem.objects.get(id=id)
        cartitem.cart.user = request.user
        cartitem.delete()
        return JsonResponse(data={"success":"Product was deleted."})
    else:
        return HttpResponseBadRequest("Invalid request.")

        
            
    
    
 
    
    

