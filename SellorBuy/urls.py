from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemaps_views
from .sitemap import StaticViewSiteMap, ProductSiteMap,CategorySiteMap
from .feeds import ProductFeed, AtomSiteNewsFeed
from django.contrib.auth import views as auth_views 
from django.views.generic.base import TemplateView

sitemaps ={
    'product' : ProductSiteMap,
    'category' : CategorySiteMap,
    'static':StaticViewSiteMap,    
    
    }



urlpatterns = [
    path("admin/", admin.site.urls),
     path('payment/', include('Payment.urls', namespace='payment')),
    path("", include("Account.urls", namespace="account")),
    path("product/", include("Product.urls",namespace="products")),
    path("order/",include("Order.urls",namespace="order")),
    path("my/",include("Customer.urls",namespace="customer")),
    path("profile/",include("Profile.urls",namespace="profile")), 
    path("shipping/",include("ShippingTracker.urls",namespace="trackshipping"))   ,
    path("cart/", include("Cart.urls",namespace="cart")),
    path("sitemap.xml",sitemaps_views.index,{"sitemaps":sitemaps}),
    path("sitemap-<str:section>.xml", sitemaps_views.sitemap, {"sitemaps":sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
      path('rss/', ProductFeed(), name="rss"),
    path('feed/',ProductFeed(), name="rss"),
    path('atom/',AtomSiteNewsFeed() , name="atom"), 
   
    path('password-reset/',auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_mail_sent.html' ),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirmation.html'
         ),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_completed.html'
         ),name='password_reset_complete'),
    
    
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


from django.conf.urls import handler500

handler404 = 'Account.views.handler_not_found'
handler500 = 'Account.views.handler_server_error'
handler400 = 'Account.views.handler_400'
handler403 = 'Account.views.handler403'