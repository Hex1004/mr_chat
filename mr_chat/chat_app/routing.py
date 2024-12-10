from django.urls import path
from mr_chat.chat_app import consumers

websocket_urlpatterns = [
    path('', consumers.ChatConsumer.as_asgi()),
]