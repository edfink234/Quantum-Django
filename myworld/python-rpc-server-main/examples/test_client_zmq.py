#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json

context = zmq.Context()

data = '{ "jsonrpc": "2.0", "method": "hello", "params": ["Max"], "id": 1}'
data2 = '{ "jsonrpc": "2.0", "method": "add_numbers", "params": [5,8], "id": 2}'
data_rpc = '{ "jsonrpc": "2.0", "method": "rpc_info", "id": 3}'

#  Socket to talk to server
print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

print('connected')
socket.send_string(data_rpc)
print('send')
#  Get the reply.
message = socket.recv_string()
print('received:', message)