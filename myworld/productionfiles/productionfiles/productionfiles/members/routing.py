from django.urls import re_path

from . import consumers

#routes consumer classes to file paths. So when you do "chat
websocket_urlpatterns = [
    re_path(r"ws/members/$", consumers.ZMQChannels.as_asgi()),
    re_path(r"ws/members/Motor_Control/Motor_Control$", consumers.ZMQChannels.as_asgi()),
    re_path(r"ws/members/Raman/Raman/", consumers.ZMQChannels.as_asgi()),
    re_path(r"ws/members/", consumers.ZMQChannels.as_asgi()),
]
