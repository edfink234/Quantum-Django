#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

#https://zeromq.org/languages/python/

import zmq
import pandas as pd
from itertools import cycle #cycle through data
import asyncio
import websockets
import sys
context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
val = 5555 + int(sys.argv[1])
socket.connect(f"tcp://localhost:{val}")

for request in cycle(range(10)):
    print("Sending request %s …" % request)
    socket.send_string("Hello")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))

#async def hello():
#    uri = "ws://localhost:8765"
#    async with websockets.connect(uri) as websocket:
#        name = "Edward"
#
#        await websocket.send(name)
#        print(f">>> {name}")

#        greeting = await websocket.recv()
#        print(f"<<< {greeting}")


#asyncio.run(hello())





