#subscriber

from channels.layers import get_channel_layer
from time import sleep
import asyncio
import zmq
import sys
import signal
import struct
from asgiref.sync import async_to_sync
from multiprocessing import Process
from shared_memory_dict import SharedMemoryDict

from threading import Thread

#Receives data from the consumer class function 'receive' which received data from the Raman.html
smd_config = SharedMemoryDict(name='config', size=1024)


async def func_receive(channel_layer):
    """
    Receives data from consumers.py ZMQChannels.receive(), i.e., the frontend

    Parameters
    ----------
    channel_layer: channels_redis.core.RedisChannelLayer
        returned by channels.layers.get_channel_layer()

    """
    global smd_config
    try:
        while True:
            x = await channel_layer.receive("ZMQ") #Waits until a message is received from the channel layer
            if smd_config.get("status"):
                if x.get('text_data')=='"increase!"':
                    smd_config["status"]+=1e-5 #increase time delay for publisher in client.py
                elif x.get('text_data')=='"decrease!"':
                    smd_config["status"]-=1e-6 #decrease time delay for publisher in client.py
            
            #via the Javascript 'signal' button
            if x.get('text_data')=='"hi friend"':
                print("🥳"*1000,end="\n\n")
            print(smd_config.get("status"), flush = True, end = "\r")
    except asyncio.CancelledError as e:
        print("Break it out")
        raise(e)

def between_callback(args):
    """
    Executed in a subprocess, stably calls func_receive 

    Parameters
    ----------
    channel_layer: channels_redis.core.RedisChannelLayer
        returned by channels.layers.get_channel_layer()

    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(func_receive(args)))
    loop.close()


#Receiving data from the camera and sending it to the group
async def TrueServerZMQ(socket, channel_layer):
    """
    Receives data from client.py, then sends it to the channel layer

    Parameters
    ----------
    socket: zmq.sugar.context.Context
        returned by zmq.Context()
    channel_layer: channels_redis.core.RedisChannelLayer
        returned by channels.layers.get_channel_layer()
    """
    while True:
        try:
            [topic, message, time] = socket.recv_multipart()
            if topic.decode() in ["MAXBOX", "CAMERA"]:
                num_floats = len(message) // struct.calcsize('f')
                data = list(struct.unpack('f' * num_floats, message))
                message = [topic.decode(), data, time.decode()]
                await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [str(i) for i in message]})
        except zmq.Again:
            continue

if __name__ == '__main__':
    ZMQ_server_context = zmq.Context()
    socket = ZMQ_server_context.socket(zmq.SUB) #subscriber
    socket.setsockopt(zmq.RCVHWM, 1000000)
    socket.connect("tcp://127.0.0.1:5558")
    ZMQ_server_loaded = True
    socket.setsockopt_string(zmq.SUBSCRIBE, "CAMERA")
    channel_layer = get_channel_layer()
    print("Here is the ",channel_layer)

    # listening in when the front end sends data back to us (subscriber)
    p = Process(target=between_callback, args=(channel_layer,))
    p.start()

    asyncio.run(TrueServerZMQ(socket, channel_layer))

        
