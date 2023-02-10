from channels.layers import get_channel_layer
from itertools import cycle
from time import sleep
import asyncio
import zmq

async def TrueServerZMQ():
    ZMQ_server_context = zmq.Context()
    socket = ZMQ_server_context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")
    ZMQ_server_loaded = True
    socket.setsockopt(zmq.SUBSCRIBE, b"CAMERA")
    channel_layer = get_channel_layer()
    print("Here is the ",channel_layer)
    for request in cycle(range(100)):
        message = socket.recv_multipart()
        await channel_layer.group_send(
                    "ZMQ",
                    {"type": "chat.message", "text": [i.decode() for i in message]},
                )

asyncio.run(TrueServerZMQ())
