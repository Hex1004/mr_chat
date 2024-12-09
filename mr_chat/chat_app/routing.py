from django.urls import re_path
from mr_chat.chat_app import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]