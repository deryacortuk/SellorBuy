from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Product.models import Products, Category
from Profile.models import Profile

class StaticViewSiteMap(Sitemap):
    priority = 0.6
    changefreq = 'daily'
    
    def items(self):
        return ["account:home",]
    def location(self,item):
        return reverse(item)
    
class ProductSiteMap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'
    
    def items(self):
        return Products.objects.filter(status="sell",is_active=True)
    def lastmod(self, obj):
        return obj.created
    
class CategorySiteMap(Sitemap):
    priority = 0.6
    changefreq = "Weekly"
    
    def items(self):
        return Category.objects.all()
    
  
    
    

    
    

    
    
    
    