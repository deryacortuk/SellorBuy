from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Cart.models import Cart, CartItem
from Order.forms import OrderForm
from Order.tasks import order_created
from django.urls import reverse
import logging
from django.contrib.auth.decorators import login_required
from Product.models import Category

logger = logging.getLogger(__name__)


def order_creates(request):    
    data = Category.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            user = request.user
            order.user = user
            order.save()
            cart_list = Cart.objects.get(user=request.user, used=False)
            products = cart_list.products.all()
            for item in products:
                OrderItem.objects.create(order=order,product=item.product,price=item.product.price,quantity=item.quantity)
            cart_list.delete()
            order_id =int(order.id)            
            order_created.delay(order_id)
            request.session['order_id'] = order.id                
            
                
            return redirect(reverse("payment:process"))
    else:
        form = OrderForm() 
        
        if Cart.objects.filter(user=request.user, used=False).exists():
            cart_list = Cart.objects.get(user=request.user, used=False)
            products = cart_list.products.all()
            return render(request,"orders/ordercheck.html",{"form":form,"products":products,"cart":cart_list,"data":data})          
                   
            
        return render(request,"orders/ordercheck.html",{"form":form,"data":data})
    
@staff_member_required
def admin_order_detail(request, order_id):
    data = Category.objects.all()
    order = get_object_or_404(Order, id=order_id)
    return render(request,'orders/admin/detail.html',{'order': order,"data":data})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/pdf.html',{'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS("C:/Users/Derya/OneDrive/Masaüstü/e-Commerce/static/css/pdf.css")])
    return response



@login_required
def order_list(request):
    data = Category.objects.all()
    user = request.user
    orders = Order.objects.filter(user=user,paid=True )
    
    return render(request,"orders/order_list.html",{"orders":orders, "data":data})
    