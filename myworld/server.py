from channels.layers import get_channel_layer
from time import sleep
import asyncio
import zmq

async def hi():
    x = await asyncio.sleep(1)
    print(f"{x} hi")

async def TrueServerZMQ():
    ZMQ_server_context = zmq.Context()
    socket = ZMQ_server_context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")
    ZMQ_server_loaded = True
    socket.setsockopt(zmq.SUBSCRIBE, b"CAMERA")
    channel_layer = get_channel_layer()
    print("Here is the ",channel_layer)
#    print(dir(channel_layer))

    
    
    while True:
        message = socket.recv_multipart()
        print(message)
        await channel_layer.group_send(
                    "ZMQ",
                    {"type": "chat.message", "text": [i.decode() for i in message]},
                )
#        try:  # block at most for one second
#            x = await asyncio.wait_for(channel_layer.receive("ZMQ"), .1)
##            print(next(x))
#        except asyncio.TimeoutError:
#            continue
#        try:
            
#        x = await channel_layer.receive("ZMQ")
#
#        print(x)
#        print("pass")
#        print(dir(x))
        

asyncio.run(TrueServerZMQ())
#asyncio.run(hi())
