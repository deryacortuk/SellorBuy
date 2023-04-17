from django.shortcuts import render, redirect
from .models import CustomerWishList
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import logging
from Product.models import Products
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import WishlistSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import  permissions, status
from Product.models import Category
from Profile.models import BankInformation
from .forms import BankCardForm

logger = logging.getLogger(__name__)

@login_required
def bankcard(request):
    data = Category.objects.all()
    form = BankCardForm()
    bank = BankInformation.objects.get(user=request.user)
    if request.method == "POST":        
        form = BankCardForm(request.POST,instance=bank)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = request.user
            user.save()
            return redirect("profile:user")
        
    return render(request,"customer/customerbankinfo.html",{"data":data,"form":form,"bank":bank})
        


@api_view(["POST"])
def add_wishlist(request, id):
    
    user = get_object_or_404(User, username=request.user)
    product = get_object_or_404(Products,id=id)    
    
    wishlist = CustomerWishList.objects.filter(user=user, product=product)
    if wishlist.exists():
        wishlist.delete()
        return Response({"id":id})
    else:
        item, created = CustomerWishList.objects.get_or_create(user=user,product=product)
        item.save()
        serializer = WishlistSerializer(data=request.data,instance=product, context={"request":request})  
        if serializer.is_valid(raise_exception=True):
            serializer.save()      
        
            return Response({"id":id})
        return Response({"id":id})
        

class WishlistAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "customer/favoritelist.html"
    def get(self,request):
        data = Category.objects.all()
        user = request.user
        wishlist = CustomerWishList.objects.filter(user=user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response({"serializer":serializer.data, "data":data})
    
@login_required
def remove_wishlist(request,id):
    if request.method =="POST": 
        wishlist = CustomerWishList.objects.get(id=id)                   
        
        if wishlist.user==request.user:
            wishlist.delete()
            return JsonResponse(data={"success":"Product was removed."})
        return HttpResponseBadRequest("invalid request.")
    else:
        
       return HttpResponseBadRequest("invalid request.")
    
    