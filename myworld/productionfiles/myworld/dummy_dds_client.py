import zmq
import time
import json

context = zmq.Context()

# Connect to the port where the server is listening
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5557")

my_freq=1
my_ampl=2
my_channel=6
my_phase=42
my_profile=128

read_channel = 0

message_set = json.dumps({ "jsonrpc": "2.0", "method": "set_output", "params":{"freq":my_freq,"ampl":my_ampl, "channel":my_channel, "phase":my_phase, "profile":my_profile}, "id": 1})
message_read = json.dumps({ "jsonrpc": "2.0", "method": "read_temperature", "params":{"channel":read_channel}, "id": 2})
message_info = json.dumps({ "jsonrpc": "2.0", "method": "rpc_info", "id": 3})

socket.send_string(message_set)
data_set = socket.recv_string()
result_set = json.loads(data_set)['result']
print(result_set)


socket.send_string(message_read)
data_read = socket.recv_string()
result_read = json.loads(data_read)['result']
print(result_read)

socket.send_string(message_info)
data_info = socket.recv_string()
result_info = json.loads(data_info)['result']
print(result_info)
