from django.urls import path,  include
from .views import (sign_in, sign_up, user_logout, activate,contact, about,
        CategoryProductAPIView, ProductIndex, searchresult,categorylist, FilterProductAPIView)

app_name = 'account'



urlpatterns = [
    path("",ProductIndex.as_view(),name="home"),
    path('signup/',sign_up, name="signup"),
    path('login/', sign_in,name="login"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', user_logout, name='logout'),     
      path('about/',about, name="about"),
       path('contact/',contact, name="contact"),
      
       path("search/",searchresult,name="search"),
       path("category/",categorylist,name="category"),
       path("category/<slug>/",CategoryProductAPIView.as_view(),name="category_detail"),       
       path("category/filter/<slug>/",FilterProductAPIView.as_view(),name="filter")
       ]
