from django.urls import path
from Order.views import admin_order_pdf, admin_order_detail,order_creates,order_list

app_name="order"

urlpatterns = [
    path("checkout/",order_creates, name="order_create"),    
    path("admin/order/<order_id>/", admin_order_detail, name="admin_order_detail"),
    path("admin/order/<order_id>/pdf/", admin_order_pdf, name="admin_order_pdf"),
    path("list/",order_list, name="order_list"),
    
   
]