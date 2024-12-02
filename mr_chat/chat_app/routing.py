from django.urls import path
from mr_chat.chat_app.consumers import ChatConsumer

websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi()),  # Route WebSocket connections to ChatConsumer
]