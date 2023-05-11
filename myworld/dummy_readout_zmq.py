import zmq
import time
import json
from channels.layers import get_channel_layer
import asyncio

context = zmq.Context()

# Connect to the port where the server is listening
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

duration = 86400
t_end = time.time() + duration

channel_layer = get_channel_layer()
print("Here is the ",channel_layer)


#Receiving data from the camera and sending it to the group
async def TrueServerZMQ(socket, channel_layer):
    while time.time() < t_end :
        try:
            message = '{ "jsonrpc": "2.0", "method": "read", "id": 3}'
            socket.send_string(message)
            data = socket.recv_string()
            result = json.loads(data)['result']
            await channel_layer.group_send("ZMQ",{"type": "chat.message", "maxbox_channels": result})
            time.sleep(0.5)
        except zmq.Again:
            continue

if __name__ == '__main__':

    asyncio.run(TrueServerZMQ(socket, channel_layer))
