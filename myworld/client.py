import zmq
from itertools import cycle
from time import sleep
import numpy as np
import csv


connectOnce = False

ZMQ_client_context = zmq.Context()
print("Connecting to hello world server…")
client_socket = ZMQ_client_context.socket(zmq.PUB)
if not connectOnce:
    client_socket.bind("tcp://127.0.0.1:5555")
    connectOnce = True

with open("members/0_data_decrystallized_noIon.csv") as f:
    reader = csv.reader(f)
    count=0
    while True:
        try:
            row1 = next(reader) # get the next line
            row1 = [float(i) for i in row1[1:]]
#            print(row1)
#            print("sent")
            client_socket.send_multipart((b"CAMERA", str(row1).encode()))
            sleep(0.025)
#            print(count)
#            count+=1
        except StopIteration:
            f.seek(0) #move the cursor back to the beginning of the file
    
