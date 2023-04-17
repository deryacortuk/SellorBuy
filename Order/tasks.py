from celery import shared_task
from django.core.mail import  get_connection, EmailMessage
from Order.models import Order
from celery.utils.log import get_task_logger

    
logger = get_task_logger(__name__)     

@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id) 
    conn = get_connection(backend='django.core.mail.backends.smtp.EmailBackend')
    subject = f'Order number: {order.id}'
    message = f'Dear {order.user.first_name}, \n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}. Your invoice will be sent by e-mail when your payment is made.Your invoice will be sent by e-mail when your payment is made. \
               \n  If you have any problems with your purchase, feel free to contact us at any time. \
             \n Thanks so much for your order! I hope you enjoy your new purchase.  \n \n Best regards, \n \n SellorBuy'
    
    mail_send = EmailMessage(subject=subject,body=message,
     from_email='sellorbuy@sellorbuy.shop',    
        to=[order.email]) 
    
    return mail_send.send()
    
    
    