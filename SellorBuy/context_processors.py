from django.conf import settings
import logging
from django.utils import timezone
from Product.models import Products, Category
from django.core.cache import cache

def website_url(request):
    return {
        "WEBSITE_URL": settings.WEBSITE_URL
    }
logger = logging.getLogger(__name__)


    
