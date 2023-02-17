from channels.layers import get_channel_layer
from time import sleep
import asyncio
import zmq
import sys
import signal
'''
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
#        print(message)
#        await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})
#
#        x = await channel_layer.receive("ZMQ")
        
        tasks = [asyncio.create_task(channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})), asyncio.create_task(channel_layer.receive("ZMQ"))]
        
        done, pending = await asyncio.wait(tasks, timeout = 0.075)
        
        for task1 in done:
            print(task1.result())
        for task2 in pending:
            try:
                print(task2.result())
            except asyncio.exceptions.InvalidStateError:
                print("failed")
                continue
                
'''
#        print("pass")
#        print(dir(x))
        

#asyncio.run(TrueServerZMQ())
#asyncio.run(hi())


async def func_group_send(socket, channel_layer):
    try:
        while True:
            message = socket.recv_multipart()
            await channel_layer.group_send("ZMQ",{"type": "chat.message", "text": [i.decode() for i in message]})
    except asyncio.CancelledError as e:
        print("Break it out")
        raise(e)
#        print(message)

async def func_receive(channel_layer):
    try:
        while True:
            x = await channel_layer.receive("ZMQ")
            print("pass")
            print(x)
    except asyncio.CancelledError as e:
        print("Break it out")
        raise(e)

def ask_exit():
    for task in asyncio.all_tasks():
        task.cancel()
    asyncio.ensure_future(exit())
        
def main():
    ZMQ_server_context = zmq.Context()
    socket = ZMQ_server_context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5555")
    ZMQ_server_loaded = True
    socket.setsockopt(zmq.SUBSCRIBE, b"CAMERA")
    channel_layer = get_channel_layer()
    print("Here is the ",channel_layer)
    
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(func_group_send(socket, channel_layer))
    asyncio.ensure_future(func_receive(channel_layer))
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, ask_exit)
    except NotImplementedError:
        pass  # Ignore if not implemented. Means this program is running in windows.
    loop.run_forever()
    loop.close()

main()


