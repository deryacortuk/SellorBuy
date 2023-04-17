from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.conf import settings
from Order.models import Order
import stripe
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

from Product.models import Category


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    data = Category.objects.all()
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:done'))
        cancel_url = request.build_absolute_uri(reverse("payment:canceled"))
        session_data = {
            "mode":"payment",
            "client_reference_id":order.id,
            "success_url":success_url,
            "cancel_url":cancel_url,
            "line_items":[]
        }
        
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data':{
                    "unit_amount": int(item.price *Decimal('100')),
                    "currency":"usd",
                    "product_data":{
                        "name":item.product.title
                    },
                },
                "quantity":item.quantity
                
            })
        session = stripe.checkout.Session.create(**session_data)
        
        return redirect(session.url, code=303)
    else:
        return render(request, "payment/payment.html",locals())
    
def payment_done(request):
    data = Category.objects.all()
    return render(request, 'payment/payment-success.html',{"data":data})
def payment_canceled(request):
    data = Category.objects.all()
    return render(request, 'payment/payment-cancel.html',{"data":data})

        
        