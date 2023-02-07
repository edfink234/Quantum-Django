import zmq
from itertools import cycle
from time import sleep

connectOnce = False

ZMQ_client_context = zmq.Context()
print("Connecting to hello world server…")
client_socket = ZMQ_client_context.socket(zmq.PUB)
print("🥹")
if not connectOnce:
    client_socket.bind("tcp://127.0.0.1:5555")
    connectOnce = True
print("😓")
#try:
print("hi")
for request in cycle(range(100)):
    print("Sending request %s …" % str(request).encode())
    client_socket.send_multipart([b"CAMERA", str(request).encode()])
    sleep(1)
        #  Get the reply.
#finally:
#    ZMQ_client_context.term()
