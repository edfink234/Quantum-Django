#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

#https://websockets.readthedocs.io/en/stable/howto/quickstart.html


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



count = 0
print("hi")

async def hello(websocket):
    global count#, users
    try:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        val = 5555 + int(sys.argv[1])
        socket.bind(f"tcp://*:{val}")
        while True:
        #    name = await websocket.recv()
        #    print(f"<<< {name}")
            message = socket.recv()
            print("hi")
        #    greeting = f"Hello {name}!"
        #
        #    await websocket.send(greeting)
        #    print(f">>> {greeting}")
            sleep(1)
    #        users.add(websocket)
            await websocket.send(json.dumps(f"hello {count} {message}"))
            socket.send_string("World")
            #get the channel layer and send it over via the channel layer
            count+=1
    finally:
        print("hi")
        context.term()
    
async def main():
    async with websockets.serve(hello, "localhost", 8765+int(sys.argv[1])):
        await asyncio.Future()  # run forever


asyncio.run(main())

