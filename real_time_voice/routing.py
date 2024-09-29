from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/process_call', consumers.CallingConsumer.as_asgi()),
]