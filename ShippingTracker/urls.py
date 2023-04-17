from django.urls import path
from .views import TrackerShipAPI, TrackerDetailAPI,add_tracking_info

app_name = "trackshipping"

urlpatterns = [
    path("",TrackerShipAPI.as_view(),name="shipping"),
    path("detail/<id>/",TrackerDetailAPI.as_view(),name="detail"),
    path("tracking/<id>/",add_tracking_info, name="add_track_info"),
]