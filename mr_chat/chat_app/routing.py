# routing.py
from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'', ChatConsumer.as_asgi()),  # Adjust the URL pattern as needed
]
