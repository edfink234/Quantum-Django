#subscriber

from channels.layers import get_channel_layer
from time import sleep
import asyncio
import zmq
import sys
import signal
from asgiref.sync import async_to_sync
from multiprocessing import Process
from shared_memory_dict import SharedMemoryDict

from threading import Thread

#Receives data from the consumer class function 'receive' which received data from the Raman.html

async def func_receive(channel_layer):
    try:
        while True:
            x = await channel_layer.receive("ZMQ")
            if smd_config.get("status"):
                if x.get('text_data')=='"increase!"':
                    smd_config["status"]+=1e-5 #increase time delay for publisher in client.py
                elif x.get('text_data')=='"decrease!"':
                    smd_config["status"]-=1e-6 #decrease time delay for publisher in client.py
            
            #via the Javascript 'signal' button
            if x.get('text_data')=='"hi friend"':
                print("🥳"*1000,end="\n\n")
            print(smd_config["status"], flush = True, end = "\r")
    except asyncio.CancelledError as e:
        print("Break it out")
        raise(e)

def between_callback(args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(func_receive(args)))
    loop.close()

smd_config = SharedMemoryDict(name='config', size=1024)
#Receiving data from the camera and sending it to the group
async def TrueServerZMQ(socket, channel_layer):
    while True:
        try:
            message = socket.recv_multipart(flags=zmq.NOBLOCK)
            await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})
        except zmq.Again:
            continue

if __name__ == '__main__':
    ZMQ_server_context = zmq.Context()
    socket = ZMQ_server_context.socket(zmq.SUB) #subscriber
    socket.setsockopt(zmq.RCVHWM, 1000000)
    socket.connect("tcp://127.0.0.1:5555")
    ZMQ_server_loaded = True
    socket.setsockopt(zmq.SUBSCRIBE, b"CAMERA")
    channel_layer = get_channel_layer()
    print("Here is the ",channel_layer)

    # listening in when the front end sends data back to us (subscriber)
    p = Process(target=between_callback, args=(channel_layer,))
    p.start()

    asyncio.run(TrueServerZMQ(socket, channel_layer))

        
