from django.contrib import admin
from ShippingTracker.models import ShipTracker



    
@admin.register(ShipTracker)
class ShippTrackerAdmin(admin.ModelAdmin):
    list_display = ["sender_shipping","recipient_shipping","tracking_number","status", "eventId","carrier_name","carrier_code","delivered_at", "destination_country" ]
    list_display_links = ["sender_shipping","recipient_shipping","tracking_number", "eventId","carrier_name", "destination_country" ]
    
    class Meta:
        model = ShipTracker