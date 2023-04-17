from django.shortcuts import render, get_object_or_404
from ShippingTracker.models import ShipTracker
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from ShippingTracker.serializers import ShipTrackerSerializer
from Product.models import Category
from django.db.models import Q
from django.http.response import  HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
import logging
from .trackerapi import TrackingShippingAPI

logger = logging.getLogger(__name__)

class TrackerShipAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "orders/shipping.html" 
    
    def get(self, request, format=None):
        data = Category.objects.all()
        user = request.user
        shipping = ShipTracker.objects.filter(Q(recipient_shipping = user)|Q(sender_shipping=user))
        serializer = ShipTrackerSerializer(shipping,many=True)
        return Response({'serializer':serializer.data,"data":data})
    
class TrackerDetailAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "orders/shipping_detail.html"
    
    def get(self, request,id, format=None):
        data = Category.objects.all()
        shipping = ShipTracker.objects.get(pk=id)
        serializer = ShipTrackerSerializer(shipping)
        trackapi = TrackingShippingAPI()
        
        trackshipping =trackapi.trackshipping(shipping.carrier_name, shipping.tracking_number)
        return Response({'serializer':serializer.data,'data':data,'track':trackapi.apiauth,"tracking":trackshipping})
        
@login_required      
def add_tracking_info(request,id):
    trackshipping = get_object_or_404(ShipTracker,pk=id)
    if request.method == "POST":
        carrier_name = request.POST.get("carriername")
        carrier_code = request.POST.get("carriercode")
        tracking_number = request.POST.get("trackingnumber")
        eventId = request.POST.get("eventid","4")
        trackshipping.carrier_name = carrier_name
        trackshipping.carrier_code = carrier_code
        trackshipping.tracking_number = tracking_number
        trackshipping.eventId = eventId
        trackshipping.save()
        # return JsonResponse({"carriercode":carrier_code,"carriername":carrier_name,"trackingnumber":tracking_number,"eventid":eventId})
        return JsonResponse("success",safe=False)
    return HttpResponseBadRequest('invalid request')
        
   
         
        
    


