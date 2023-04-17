from django.db import models
from Order.models import Order
from django.utils.translation import gettext_lazy as _ 
import logging

# logger = logging.getLogger(__name__)

# class Payment(models.Model):
#     PENDING = "P"
#     COMPLETED = "C"
#     FAILED = "F"
    
#     STATUS_CHOICES = (
#         (PENDING,_("pending")), (COMPLETED,_("completed")), (FAILED,_("failed"))
#         )
    

#     status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)
#     order = models.OneToOneField(Order, related_name="payment",on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         ordering = ("-created_at")
        
#     def __str__(self):
#         return self.order.buyer.get_full_name()


