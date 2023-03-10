import zmq
from itertools import cycle
from time import sleep, time
import numpy as np
import csv
from shared_memory_dict import SharedMemoryDict


connectOnce = False

smd_config = SharedMemoryDict(name='config', size=1024)
ZMQ_client_context = zmq.Context()
print("Connecting to hello world server…")
client_socket = ZMQ_client_context.socket(zmq.PUB)
if not connectOnce:
    client_socket.bind("tcp://127.0.0.1:5555")
    connectOnce = True

sleep(1)
with open("members/0_data_decrystallized_noIon.csv") as f:
    reader = csv.reader(f)
    count=0
    while True:
        try:
            row1 = next(reader) # get the next line
            row1 = [float(i) for i in row1[1:]]
#            print(row1)
#            print("sent")
            smd_config["status"] = False
            client_socket.send_multipart((b"CAMERA", str(row1).encode(),str(time()).encode()))
#            print("sent")
#            while True:
#                try:
#                    smd_config["status"]
#                    break
#                except KeyError:
#                    continue
#            print(smd_config["status"])
#            while not smd_config["status"]:
#                pass
#                client_socket.send_multipart((b"CAMERA", str(row1).encode(),str(time()).encode()))
#                print(count)

#                count+=1
#            print(count)
#            break
            
#            while True:
#                try:
#                    smd_config["group_send_status"]
#                    break
#                except KeyError:
#                    continue
#            print(str(row1).encode(),str(time()).encode())
            while not smd_config["status"]:
                pass
##                print(smd_config.get("status"))
#                client_socket.send_multipart((b"CAMERA", str(row1).encode(),str(time()).encode()))
#
##                print("\n\n")
#                print("stuck")
            sleep(0.02)
#            print("hi")
#            print(time())
#            print(count)
#            count+=1
        except StopIteration:
            f.seek(0) #move the cursor back to the beginning of the file

