from django.urls import path
from .views import (ProductDetail, ProductCreateSell,delete_product, SecondhandProductAPIView,FilterSecondhandAPIView,
ListUserProductAPIView,ProductUpdateAPIView, comment_product, delete_review,FilterPriceSecondhandAPIView,SellerListProductAPIView)

app_name = "products"

urlpatterns = [    
    path("secondhand/",SecondhandProductAPIView.as_view(),name="secondhand"),             
    path("shop/sell/",ProductCreateSell.as_view(),name="sell"),     
    path("sell/user/", ListUserProductAPIView.as_view(),name="sell_list"),    
    path("comment/product/",comment_product, name="comment"),    
     path("<slug>/",ProductDetail.as_view(),name="product_detail"),
     path("update/<pk>/",ProductUpdateAPIView.as_view(),name="update"),
    path("delete/<id>/",delete_product, name="delete"),
    path("comment/delete/<id>/",delete_review, name="comment_delete"),
    path("secondhand/<slug>/",FilterSecondhandAPIView.as_view(),name="filter_secondhand"),
    path("filter/secondhand/",FilterPriceSecondhandAPIView.as_view(),name="filter_price"),
    path("seller/@<username>/",SellerListProductAPIView.as_view(),name="seller_products"),
   
   
     
]