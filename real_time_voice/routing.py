from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/calling/(?P<room>.*)', consumers.CallingConsumer.as_asgi()),
]