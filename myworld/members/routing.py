# chat/routing.py
from django.urls import re_path
#from channels.routing import ProtocolTypeRouter, URLRouter
#from django.core.asgi import get_asgi_application
#from .demultiplexer import Demultiplexer

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/members/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/members/$", consumers.PlotlyConsumer.as_asgi()),
    re_path(r"ws/members/$", consumers.TestData.as_asgi()),
    re_path(r"ws/members/data/data/$", consumers.TestDataAutomatic.as_asgi()),
    re_path(r"ws/members/Motor_Control/Motor_Control$", consumers.PlotlyConsumer.as_asgi()),
    re_path(r"ws/members/Raman/Raman/", consumers.ZMQChannels.as_asgi()),
#    re_path(r"ws/members/Raman/Raman/", Demultiplexer.as_asgi()),
]

#application = ProtocolTypeRouter({
#    "http": get_asgi_application(),
#    "websocket": URLRouter([
#        re_path(r"^/$", Demultiplexer.as_asgi()),
#    ])
#})
