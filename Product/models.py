from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
from mptt.models import MPTTModel, TreeForeignKey
from Product.imageutils import compress, thumnail, midcompress
from django.db.models import Q

import logging




logger = logging.getLogger(__name__)

class Category(MPTTModel):
    title = models.CharField(max_length=20,)
    slug = models.SlugField(max_length=20, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    description = models.CharField(max_length=50)

    class MPTTMeta:          
        order_insertion_by = ['title']
    
        
    def get_absolute_url(self):
        return reverse('account:category_detail', args=[self.slug])
    def __str__(self):
        
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return " > ".join(full_path[::-1])
            
 
    
    def __unicode__(self):
        return self.title       
    @property
    def get_products(self):
        return Products.objects.filter(category__slug=self.slug)            


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)           
        super(Category, self).save(*args, **kwargs)    
    @property
    def structured_data(self):
        from django.utils.translation import get_language
        lang_code = get_language()
        
        data = {
            "@type":"Creativework",
            "name":self.title,
            "desctiption": self.description,
            "inLanguage": lang_code,
        }
                  
        return data 




    

class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def filter_products(self, keyword,min_price, max_price):
        qs = self.get_queryset().filter(is_active=True,status="sell",quantity__lte=1)
        if keyword:
            qs = qs.filter(
                Q(category__title__icontains=keyword)
            ).distinct()
            
        
        if max_price:
            max_price = int(max_price)
            qs = qs.filter(price__lte=max_price)
        if min_price:
            min_price = int(min_price)
            qs = qs.filter(price__gte = min_price)
        return qs
    
      
def product_directory_path(instance):   
    return 'seller_{0}'.format(instance.seller.id) 
def image_thumnail_path(instance,filename):
    return 'thumnail_seller_{0}'.format(instance.seller.id)
def image_mid_path(instance,filename):
    return 'midimg_seller_{0}'.format(instance.seller.id)

class Products(models.Model):
    SELL = 'sell'
    SOLDOUT = 'soldout'
    STATUS_CHOICES = ((SELL,_('sell')),(SOLDOUT,_('soldout')))
    
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to=product_directory_path, null=False)
    image2 = models.ImageField(upload_to=product_directory_path, null=True,blank=True)
    image3 = models.ImageField(upload_to=product_directory_path, null=True,blank=True)
    description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    is_active=models.BooleanField(default=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=10, default=SELL)
    quantity = models.IntegerField(default=1)    
    views = models.IntegerField(default=0)  
    tax = models.DecimalField(max_digits=4, decimal_places=2, default= 0) 
    secondhand = models.BooleanField(default=False)
    brand = models.CharField(max_length=100,null=True, blank=True)
    size = models.CharField(max_length=10,null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    img_thumbnail = models.ImageField(upload_to=image_thumnail_path,null=True, blank=True)
    img2_thumbnail = models.ImageField(upload_to=image_thumnail_path,null=True,blank=True)
    img3_thumbnail = models.ImageField(upload_to=image_thumnail_path,null=True, blank=True)
    img_mid = models.ImageField(upload_to=image_mid_path,null=True, blank=True)
    img2_mid = models.ImageField(upload_to=image_mid_path,null=True,blank=True)
    img3_mid = models.ImageField(upload_to=image_mid_path,null=True, blank=True)    
    
    
           
    objects = ProductManager()

    class Meta:
        ordering = ('-created',)
        index_together = (('id','slug'))
        
        
        
    def __str__(self):
        return self.title
       
    
    
    
    def save(self, *args, **kwargs):
        self.price = round((self.product_price * 0.2) + self.product_price,2)
        self.image = compress(self.image)
        self.img_thumbnail = thumnail(self.image)
        self.img_mid = midcompress(self.image)
        if Products.objects.filter(title = self.title).exists():
            extra = str(randint(1, 1000))
            self.slug = slugify(self.title) + "-" + extra
        else:
            self.slug = slugify(self.title,allow_unicode=True)
       
        if bool(self.image2):
            self.image2 = compress(self.image2)
            self.img2_thumbnail = thumnail(self.image2)
            self.img2_mid = midcompress(self.image2)
        if bool(self.image3):
            self.image3 = compress(self.image3)
            self.img3_thumbnail = thumnail(self.image3)
            self.img3_mid = midcompress(self.image3)
            
        if self.quantity == 0:
            self.is_active = False  
            self.status = "soldout"          
        super(Products, self).save(*args, **kwargs)
        
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])
    
    @property
    def structured_data(self):
        from django.utils.translation import get_language
        lang_code = get_language()
        
        data = {
            "@type":"Creativework",
            "name":self.title,
            "desctiption": self.description,
            "inLanguage": lang_code,
        }
        if self.seller:
            data["seller"] = {
                "@type":"Person",
                "name":self.seller.get_full_name() or self.seller.username
            }
        if self.image:
            data["image"] = self.image.url            
        return data
    
    
    
    def get_related_products(self):
        title_split = self.title.split(' ')
        lookups = Q(title__icontains=title_split[0])
        
        for i in title_split[1:]:
            lookups |= Q(title__icontains=i)
        
        
        related_products = Products.objects.filter(lookups).distinct().exclude(id=self.id)
        return related_products
    


class ProductTransaction(models.Model):
    
    transaction_type_choices=((1,"BUY"),(2,"SELL"))
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    transaction_type=models.CharField(choices=transaction_type_choices,max_length=20)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ("-created_at",)
    def __str__(self):
        return str(self.product_id)
    

    
class ProductReviews(models.Model):
    
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)    
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)    
    rating=models.CharField(default="0",max_length=255,null=True, blank=True)
    review=models.TextField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("created_at",)
        
    def __str__(self):
        return str(self.product_id)
    
import uuid

class ProductViews(models.Model):
    uuid = models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    ip = models.CharField(max_length=250)
    product = models.ForeignKey(Products, related_name="product_views",on_delete=models.CASCADE)
    
    
