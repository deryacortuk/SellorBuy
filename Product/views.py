from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import  permissions, status
from django.shortcuts import get_object_or_404,redirect
from .serializers import ( ProductReviewsSerializer,ProductsReadSerializer,ProductWriteSerializer, CategoryReadSerializer)
from .models import Products, ProductReviews,  Category, ProductViews
import logging
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, JsonResponse
# from Order.recommender import Recommender
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


from django.views.generic import ListView

logger = logging.getLogger(__name__)

def recently_viewed(request,pk):
    if not "recently_viewed" in request.session:
        request.session["recently_viewed"] = []
        request.session["recently_viewed"].append(pk)
    else:
        if pk in request.session["recently_viewed"]:
            request.session["recently_viewed"].remove(pk)
        request.session["recently_viewed"].insert(0, pk)
        if len(request.session["recently_viewed"]) > 5:
            request.session["recently_viewed"].pop()
    request.session.modified = True   

class ProductDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/product_detail.html'
    permission_classes = (permissions.AllowAny,)
    style = {'template_pack': 'rest_framework/vertical/'}
    
    # @method_decorator(cache_page(60))
    # @method_decorator(vary_on_cookie)
    def get(self, request,slug):
        data = Category.objects.all()
        product = get_object_or_404(Products,slug=slug)
        
        quantity = [(i, str(i)) for i in range(1, product.quantity+1)]
        serializer = ProductsReadSerializer(product,context= {'request': request})
        
        recently_viewed(request, product.pk)
        
        
        
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        
        
        
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
            
        if not ProductViews.objects.filter(product=product, ip=ip).exists():
            ProductViews.objects.create(product=product, ip=ip)
            product.views += 1
            product.save()
        username = product.seller.username
        reviews = ProductReviews.objects.filter(product_id = product)
        related_products = ProductsReadSerializer(product.get_related_products(),many=True,context={"request":request})
        serializer_review = ProductReviewsSerializer(reviews,context= {'request': request},many=True)
        return Response({'serializer': serializer.data, "username":username,'reviews': serializer_review.data, "quantity":quantity,"data":data,"related_products":related_products.data})
    
    
            
class ProductUpdateAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product/product_update.html"       
    
    def get(self, request, pk):  
        data = Category.objects.all()    
        product = get_object_or_404(Products,id=pk)
        serializer = ProductWriteSerializer(product)
        return Response({'serializer': serializer,"id":pk,"product":product,"data":data})    
    def post(self, request, pk):        
        product = get_object_or_404(Products, id=pk)        
        serializer = ProductWriteSerializer(product, data=request.data, context={"request":request})        
        if serializer.is_valid(raise_exception=True):            
            serializer.save()            
            return redirect("products:sell_list")
        else:
            return Response({'serializer': serializer, 'product': product,"id":pk})
        
    

class ListUserProductAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product/seller_products.html"
    
    @method_decorator(cache_page(60))
    def get(self, request):
        user = request.user
        data = Category.objects.all()
        products = Products.objects.filter(seller=user)
        serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
        return Response({'serializer':serializer.data,"data":data})
    
class SellerListProductAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product/sellerproductlist.html"
    
    @method_decorator(cache_page(60))
    def get(self, request, username):
        user = get_object_or_404(User,username=username)
        data = Category.objects.all()
        products = Products.objects.filter(seller=user)
        serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
        return Response({'serializer':serializer.data,"data":data, "user":user})
        
class SecondhandProductAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product/secondhands.html"
#     """
# Furniture
# Watches
# Sporting Goods
# Electronics
# Books
# Musical Instruments
# Tools & Home Care Items
#     """
    
    # @method_decorator(cache_page(60))
    def get(self, request):  
        data = Category.objects.all()    
        
        recently_views = Products.objects.filter(pk__in=request.session.get("recently_viewed",[])) 
        products = Products.objects.filter(secondhand=True,status="sell",is_active=True).filter(quantity__gte=1)               
        
        serializer = ProductsReadSerializer(products, many=True,context={"request":request})
        return Response({'serializer':serializer.data,"data":data,"recently_views":recently_views})  
       
class FilterSecondhandAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product/secondhands.html"
    
    # @method_decorator(cache_page(60))
    def get(self, request,slug):
        
        data = Category.objects.all()
        category = Category.objects.get(slug=slug)       
        
        top_related = Products.objects.filter(is_active=True,status="sell",secondhand=True).filter(category__in=category.get_descendants(include_self=True)).order_by("-views")[:6]
        recently_views = Products.objects.filter(pk__in=request.session.get("recently_viewed",[])) 

        products = Products.objects.filter(status="sell",is_active=True,secondhand=True).filter(category__in=category.get_descendants(include_self=True)) 
        serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
        return Response({'serializer':serializer.data,"data":data,"slug":slug,"title":category.title,"recently_views":recently_views,"top_related":top_related})
    
class FilterPriceSecondhandAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "product/secondhands.html"
    
    # @method_decorator(cache_page(60))
    def get(self, request):
        
        data = Category.objects.all()
        slug = self.request.GET["category"]
        minprice = self.request.GET.get("minprice")
        maxprice = self.request.GET["maxprice"]
        recently_views = Products.objects.filter(pk__in=request.session.get("recently_viewed",[])) 
        if bool(slug):          
            
            category = Category.objects.get(slug=slug) 
            top_related = Products.objects.filter(is_active=True,status="sell",secondhand=True).filter(category__in=category.get_descendants(include_self=True)).order_by("-views")[:6]
            products = Products.objects.filter_products(category.title,minprice, maxprice).filter(secondhand=True) 
            serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
            return Response({'serializer':serializer.data,"data":data,"recently_views":recently_views,"top_related":top_related})
        else:
            top_related = Products.objects.filter(is_active=True,status="sell",secondhand=True).order_by("-views")[:6]
            products = Products.objects.filter(is_active=True,status="sell",secondhand=True)
         
            products = Products.objects.filter_products(keyword=None,min_price=minprice,max_price=maxprice).filter(secondhand=True) 
            serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
            return Response({'serializer':serializer.data,"data":data,"recently_views":recently_views,"top_related":top_related})
            
        
        
               
        
class ProductCreateSell(APIView):
     
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product/product_sell.html' 
    serializer_class = ProductWriteSerializer   
    style = {'template_pack': 'rest_framework/vertical/'}
    
    def get(self, request,format=None):           
        serializer = ProductWriteSerializer()
        data = Category.objects.all()
        return Response({'serializer': serializer, 'style': self.style,"data":data})          
   
  
    def post(self, request):                    
       
        serializer = ProductWriteSerializer(data=request.data,context={'request': request}, many=False)      
                       
        if serializer.is_valid(raise_exception=True):            
            serializer.save()
            
            return redirect("products:sell_list")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





@login_required
def delete_product(request,id):
    if request.method =="POST":
        product = Products.objects.get(id=id)
        product.seller.username = request.user.username
   
        product.delete()
        return JsonResponse(data={"success":"Product was deleted."})
    else:
        
       return HttpResponseBadRequest("invalid request.")
    


@login_required
def comment_product(request):
    if request.method == "POST":
        id = request.POST.get("id")
        
        product_id = Products.objects.get(id=id)
        user = request.user
        content = request.POST.get("content")
        rating = request.POST.get("rating","1")
        review_product = ProductReviews(product_id=product_id,user_id=user,review=content)
        review_product.rating = rating        
        review_product.save()        
        return JsonResponse("success", safe=False)
    return HttpResponseBadRequest('invalid request')
        
@login_required
def delete_review(request,id):
    if request.method =="POST": 
        review = ProductReviews.objects.get(id=id)      
                    
        
        if request.user.username == review.user_id.username:
            review.delete()
            return JsonResponse(data={"success":"Product was removed."})
        return HttpResponseBadRequest("invalid request.")
    else:
        
       return HttpResponseBadRequest("invalid request.")

    


    

