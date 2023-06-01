#publisher

import zmq
from itertools import cycle
from time import sleep, time
import numpy as np
import csv
from shared_memory_dict import SharedMemoryDict #Get rid of me during production

connectOnce = False

smd_config = SharedMemoryDict(name='config', size=1024) #Get rid of me during production, just delays 
ZMQ_client_context = zmq.Context()
print("Connecting to hello world server…")
client_socket = ZMQ_client_context.socket(zmq.PUB)
client_socket.setsockopt(zmq.SNDHWM, 1) #set high-water mark to 1
if not connectOnce:
    client_socket.bind("tcp://127.0.0.1:5555") #connect to local host
    connectOnce = True

sleep(1)

with open("members/1_data_crystallized_oneIon.csv") as f:
    reader = csv.reader(f)
    count=0
    smd_config["status"] = 0.025 #Get rid of me during production, just delays publisher
    print(smd_config["status"])
    while True:
        try:
            row1 = next(reader) # get the next line
            row1 = [float(i) for i in row1[1:]] #only process the second to last numbers in each row
            sleep(smd_config["status"]) #Get rid of me during production, just delays publisher
            client_socket.send_multipart((b"CAMERA", str(row1).encode(),str(time()).encode()))
            
        except StopIteration:
            f.seek(0) #move the cursor back to the beginning of the file

