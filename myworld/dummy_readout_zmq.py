import zmq
import time
import json
from channels.layers import get_channel_layer
import asyncio
import struct

context = zmq.Context()

# Connect to the port where the server is listening
socket = context.socket(zmq.SUB)

socket.setsockopt(zmq.RCVHWM, 1000000)
socket.connect("tcp://127.0.0.1:5556")
socket.setsockopt(zmq.SUBSCRIBE, b"MAXBOX")

channel_layer = get_channel_layer()
print("Here is the ",channel_layer)


#Receiving data from the camera and sending it to the group
async def TrueServerZMQ(socket, channel_layer):
    while True :
        try:
            message = socket.recv_multipart(flags=zmq.NOBLOCK)
            message = socket.recv()
            name = message.decode()
            message = socket.recv()
            values = struct.unpack('f' * (len(message) // 4), message)
            message = socket.recv()
            timestamp = float(message)
            
            
            await channel_layer.group_send("ZMQ",{"type": "chat.message", "maxbox_channels": values})

        except zmq.Again:
            continue

if __name__ == '__main__':

    asyncio.run(TrueServerZMQ(socket, channel_layer))
