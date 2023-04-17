from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from Product.models import Products
from django.utils.feedgenerator import Atom1Feed
from  django.utils import timezone

class ProductFeed(Feed):
    
    feed_type = Rss201rev2Feed
    description = "eCommerce website"
    description_template = "index.html"
    title = "eCommerce site"
    link = "/feed/"

    
    def items(self, obj):
        return Products.objects.filter(status="sell",is_active=True)
    
    def item_title(self,obj):
        return obj.title 
   
    def item_link(self, obj):
        return obj.get_absolute_url()
    
    def item_pubdate(self,item):
        return item.created
    def item_description(self,item):
        return item.description()
    
    def feed_copyright(self):
        now = timezone.now()
        return "Copyright© {year}".format(year=now.year)
    def item_quid(self, item):
        return 
    
class AtomSiteNewsFeed(ProductFeed):
     feed_type = Atom1Feed
     subtitle = ProductFeed.description