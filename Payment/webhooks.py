import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Order.models import Order
from .tasks import payment_completed, payment_seller_completed
from Product.models import Products
from django.shortcuts import get_object_or_404
from ShippingTracker.models import ShipTracker
import os 
import dotenv

env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '.env')
dotenv.read_dotenv(env_file)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            order.paid = True
            order.status = 'paid'  
                          
            
            order.stripe_id = session.payment_intent        
     
 
    
   
    
   

             
            for item in order.items.all():                
                
                product = get_object_or_404(Products, id= item.product.id)
                 
                shiptracker = ShipTracker(recipient_shipping =order.user,sender_shipping=product.seller,order_ship=product) 
                shiptracker.recipient_address = order.address
                shiptracker.phone_number = order.phone_number
                if order.state:
                    shiptracker.state = order.state
                shiptracker.city = order.city
                if order.comment:
                    shiptracker.comment = order.comment
                shiptracker.destination_country = order.country
                shiptracker.zip_code = order.zip_code
                if order.appartment:
                    shiptracker.appartment = order.appartment
                if order.district:
                    shiptracker.district = order.district 
                shiptracker.email = order.email
                shiptracker.quantity = item.quantity                                                             
                                            
                shiptracker.save()
                
                product.quantity -= item.quantity 
                
                if product.quantity == 0:
                    product.status = "soldout"
                    product.is_active = False
                 
                
                payment_seller_completed.delay(product.id)
                product.save()  
                
            order.save() 
            payment_completed.delay(order.id)
            
                
    return HttpResponse(status=200)