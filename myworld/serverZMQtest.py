from channels.layers import get_channel_layer
from time import time, sleep
import zmq
import sys
import asyncio
import websockets
import ssl
import pathlib
import datetime
import json
import sys
from asgiref.sync import async_to_sync

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
channel_layer = get_channel_layer()

while True:
    message = socket.recv()
    print(message)
    sleep(1)
    async_to_sync(channel_layer.group_send)(
            "ZMQ",
            {"type": "chat.message", "text": request},
        )
    socket.send_string("World")
