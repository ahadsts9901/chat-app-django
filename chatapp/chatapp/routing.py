from django.urls import re_path
import chatapp.consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<user_id>\d+)/$", chatapp.consumers.ChatConsumer.as_asgi()),
]
