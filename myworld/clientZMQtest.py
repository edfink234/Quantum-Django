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
socket.connect(f"tcp://localhost:5555")

for request in cycle(range(10)):
    print("Sending request %s …" % request)
    socket.send_string("Hello")

    #  Get the reply.
    message = socket.recv()
    print("Received reply %s [ %s ]" % (request, message))
