from django.urls import re_path, path
from .consumers import LogConsumer

websocket_urlpatterns = [
    path("ws/logs/", LogConsumer.as_asgi()),
]
