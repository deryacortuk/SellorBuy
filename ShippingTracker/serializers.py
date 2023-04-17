from rest_framework import serializers
from ShippingTracker.models import ShipTracker

class ShipTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipTracker
        fields = '__all__'
        depth = 1