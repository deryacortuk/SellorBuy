from django.shortcuts import render,redirect
import logging
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .token import account_activation_token
from django.views.decorators.cache import never_cache
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework import viewsets , permissions
from django.utils.encoding import force_str, force_bytes
from django.contrib.postgres.search import SearchQuery,SearchRank,SearchVector
from django.views.generic import ListView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404,redirect
from Product.serializers import ProductsReadSerializer, ProductReviewsSerializer
from Product.models import Products, ProductReviews, ProductTransaction, Category
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from rest_framework.pagination import LimitOffsetPagination
from Cart.models import Cart

logger = logging.getLogger(__name__)

def categorylist(request):
    category = Category.objects.all()
    
    
    return render(request,"base.html",{"data":category})





class CategoryProductAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "category.html"
    
    # @method_decorator(cache_page(60))
    def get(self, request, slug):
        
        data = Category.objects.all()
        category = Category.objects.get(slug=slug)
        products = Products.objects.filter(quantity__gte=1, is_active=True).filter(category__in=category.get_descendants(include_self=True))
 
        top_related = Products.objects.filter(is_active=True,status="sell").filter(category__in=category.get_descendants(include_self=True)).order_by("-views")[:6]
        recently_views = Products.objects.filter(pk__in=request.session.get("recently_viewed",[])) 
        serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
        return Response({'serializer':serializer.data,"data":data,"slug":slug,"title":category.title,"description":category.description,"recently_views":recently_views,"top_related":top_related})


class FilterProductAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "category.html"
    
    # @method_decorator(cache_page(60))
    def get(self, request, slug):
        
        data = Category.objects.all()
        category = Category.objects.get(slug=slug)       
        
        top_related = Products.objects.filter(is_active=True,status="sell").filter(category__in=category.get_descendants(include_self=True)).order_by("-views")[:6]
        recently_views = Products.objects.filter(pk__in=request.session.get("recently_viewed",[])) 
        minprice = self.request.GET.get("minprice")
        maxprice = self.request.GET["maxprice"]
        products = Products.objects.filter_products(category.title,minprice, maxprice)
        serializer = ProductsReadSerializer(products,context={"request":request}, many=True)
        return Response({'serializer':serializer.data,"data":data,"slug":slug,"title":category.title,"recently_views":recently_views,"top_related":top_related})



    
def searchresult(request):
    data = Category.objects.all()
    query = request.GET.get("q")
    search_vector = SearchVector("title",weight="A") + SearchVector("description", weight="B")        
    search_query = SearchQuery(query)
    products = Products.objects.filter(status="sell",is_active=True).annotate(rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.3).order_by("-rank")
    return render(request,"search.html",{"data":data,"products":products})
        
    

def sign_up(request):
    form = RegisterForm()
    data = Category.objects.all()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        to_email = request.POST.get("email")
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request).domain 
            subject = "Activation Your Account"
            
            message = render_to_string('account/activation_account_email.html', {
                "user":user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token":account_activation_token.make_token(user)                     
                                       
                                       })
            send_mail(subject, message,"sellorbuy@sellorbuy.shop" ,[to_email],fail_silently=False)
            
            return render(request, "account/activation_email_sent.html",{"user":user,"data":data})
        else:
            return render(request, "account/signup.html",{"form":form,"data":data})
    return render(request, "account/signup.html",{"form":form,"data":data})
    
def activate(request, uidb64, token, backend = 'django.contrib.auth.backends.ModelBackend'):
    data = Category.objects.all()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
       
        return render(request, 'account/activation_email_success.html',{"data":data})
    else:
        return render(request,"account/activation_email_invalid.html",{"data":data})
    
def sign_in(request):
    form = LoginForm()
    data = Category.objects.all()
    if request.method == "POST":
        form = LoginForm(request.POST) 
               
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    logger.info(REDIRECT_FIELD_NAME)
                    login(request, user)
                    return redirect("account:home")
                else:
                    messages.info(request, "Please activate your account. Activation mail was sent.")
        else:
            messages.info(request, "Please check your information")
    return render(request,"account/login.html", {"form":form,"data":data})

@never_cache   
def user_logout(request):
    logout(request)
    return redirect("account:home")
            



class ProductIndex(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account/index.html'
    
    # @method_decorator(cache_page(60*60*1))
    # @method_decorator(vary_on_cookie)
    def get(self, request):       
        data = Category.objects.all()
        # category = get_object_or_404(Category, slug="tea")
        # products = Products.objects.filter(status="sell",is_active=True).filter(category__in=category.get_descendants(include_self=True))
        # latest = Products.objects.filter(status="sell", is_active=True)[:17]        
        # latest_products = ProductsReadSerializer(latest,many=True,context={"request":request}) 
        # queryset = ProductsReadSerializer(products,many=True,context={"request":request})  
        # popular = Products.objects.filter(status="sell",is_active=True).order_by("-views")[:17]
        # popular_products = ProductsReadSerializer(popular,many=True, context={"request":request})
        
        return Response({"data":data})
        return Response({'products': queryset.data, "data":data,"latest":latest_products.data,"popular":popular_products.data})



def about(request):
    data = Category.objects.all()
    return render(request, "about.html",{"data":data})

from django.core.mail import send_mail

def contact(request):
    data = Category.objects.all()
    if request.method == "POST":
        message_name = request.POST['name']
        message_email = request.POST['email']
        message_content = request.POST['content']
        
        email_send = EmailMessage(
        subject=message_name, 
        body=message_content, 
        from_email='sellorbuy@sellorbuy.shop',  
        to=['sellorbuy@sellorbuy.shop'],
        reply_to=[message_email])     
        
        email_send.send()
        message = "Thank you for contacting us. We will contact you very soon! "
        return render(request, 'contact.html',{'message':message, "data":data})
        
    return render(request,'contact.html',{"data":data})

    

def handler_not_found(request,exception):
    data = Category.objects.all()
    return render(request,'404.html',{"data":data})

def handler_server_error(request):
    data = Category.objects.all()
    return render(request,'500.html',{"data":data})


    
def handler_400(request,exception):
    data = Category.objects.all()
    return render(request, '400.html',{"data":data})

def handler403(request,exception):
    data = Category.objects.all()
    return render(request, '403.html', {"data":data})
