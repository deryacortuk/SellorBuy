from django.urls import path
from .views import  WishlistAPIView, add_wishlist, remove_wishlist,bankcard

app_name = "customer"

urlpatterns = [
    path("add/<id>/",add_wishlist, name="addlist"),
    path("wishlist/shop/",WishlistAPIView.as_view(),name="wishlist"),
    path("remove/<id>/", remove_wishlist, name="remove_wishlist"),
    path("bank/",bankcard, name="bankinfo"),
    
]