# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/members/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/members/$", consumers.PlotlyConsumer.as_asgi()),
    re_path(r"ws/members/$", consumers.TestData.as_asgi()),
    re_path(r"ws/members/data/data/$", consumers.TestDataAutomatic.as_asgi()),
    re_path(r"ws/members/Motor_Control/Motor_Control$", consumers.PlotlyConsumer.as_asgi()),
]
