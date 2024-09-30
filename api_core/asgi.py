"""
ASGI config for api_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from djx_websocket import routing as djx_websocket_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_core.settings')
django_asgi_application = get_asgi_application()

from real_time_voice import routing as real_time_voice_routing

application = ProtocolTypeRouter({
    "http": django_asgi_application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            djx_websocket_routing.websocket_urlpatterns +
            real_time_voice_routing.websocket_urlpatterns
        )
    ),
})
