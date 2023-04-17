from django.urls import path
from Cart.views import   add_cart, CartListAPIView,delete_product, cart_quantity
app_name="cart"

urlpatterns = [
  
    # path("checkout/", CheckoutProductCart.as_view(),name="checkout"),
    path("add/<id>", add_cart, name="add_cart"),
    path("cart/list/", CartListAPIView.as_view(),name="cart_list"),
    path("delete/<id>/",delete_product, name="delete_product"),
    path("changecart/",cart_quantity, name="quantity_change")
    
    
]