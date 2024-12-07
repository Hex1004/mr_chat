"""
ASGI config for mr_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from mr_chat.chat_app import routing

# Ensure the settings module is set before importing `get_asgi_application`.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mr_chat.settings')

# Create the ASGI application.
django_asgi_app = get_asgi_application()

# Define the application instance for ASGI.
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})