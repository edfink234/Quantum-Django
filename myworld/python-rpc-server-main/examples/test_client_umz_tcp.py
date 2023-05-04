import socket
import time

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 1234)
sock.connect(server_address)

message = '{ "jsonrpc": "2.0", "method": "hello", "params": ["Max"], "id": 1}'
# message = '{ "jsonrpc": "2.0", "method": "rpc_info", "id": 3}'

mlength = str(len(message)).zfill(4)

sock.sendall(mlength.encode('utf-8') + message.encode('utf-8'))
data = sock.recv(4)
size = int.from_bytes(data, byteorder='big')
data = sock.recv(size)
print(data)