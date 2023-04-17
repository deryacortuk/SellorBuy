from django.urls import path
from notifications.consumer import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notifications/<str:username>/", NotificationConsumer)
]