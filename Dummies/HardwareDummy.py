import numpy as np
import zmq
import time
import struct
import random
import csv

# init as publisher
ZMQ_client_context = zmq.Context()


maxbox_socket = ZMQ_client_context.socket(zmq.PUB)
# TODO check if we need this
#set high-water mark to 1
#client_socket.setsockopt(zmq.SNDHWM, 1)
maxbox_socket.bind("tcp://127.0.0.1:5556")

weather_socket = ZMQ_client_context.socket(zmq.PUB)
weather_socket.bind("tcp://127.0.0.1:5557")

camera_socket = ZMQ_client_context.socket(zmq.PUB)
camera_socket.bind("tcp://127.0.0.1:5558")


print('started server...')


def publish(socket, name, message):
    socket.send_multipart([name.encode(), message, str(time.time()).encode()])

def float_to_bytes(f):
    return struct.pack('!f', f)

def list_to_bytes(l):
    return struct.pack('f' * len(l), *l)


# MAXBOX DUMMY
def maxbox_read():
    """
    Returns an array of all values with the newest read voltages.
    Keep in mind that it takes 500ms for a full read cycle of all channels.

    Returns
    -------
    array
        voltages read from the sensor
    """
    # generate random numbers as dummy output
    values = np.random.rand(16).tolist()

    return list_to_bytes(values)

# WEATHER DUMMY
def temperature():
    temperature = random.uniform(20, 23)
    return float_to_bytes(round(temperature, 2))

def pressure():
    pressure = random.uniform(980,1040)
    return float_to_bytes(round(pressure, 3))

# DDS DUMMY

# CAMERA DUMMY
class Camera:
    def __init__(self):

        self.path = ''
        self.files = ['0_data_decrystallized_noIon.csv', '1_data_crystallized_oneIon.csv', '2_data_crystallized_two_ions.csv','3_data_decrystallized_hot.csv', '4_data_decrystallized_cloud.csv']
        self.count = 0
        self.choice = random.randint(0,4)

    def camera_output(self):

        with open(self.path + self.files[self.choice]) as f:
            reader = csv.reader(f)

            try:
                for i in range(self.count+1):
                    row1 = next(reader) # get the next line

            except StopIteration:
                f.seek(0) #move the cursor back to the beginning of the file
                row1 = next(reader) #send first row
                self.count = 0
                self.choice = random.randint(0,4) # change randomly to other camera picture
            
            row1 = [float(i) for i in row1[1:]] #only process the second to last numbers in each row
            self.count += 1
            return list_to_bytes(row1)

Cam_Dummy = Camera()



while True:

    publish(maxbox_socket, 'MAXBOX', maxbox_read())
#
    publish(weather_socket, 'TEMPERATURE', temperature())
    publish(weather_socket, 'PRESSURE', pressure())

    publish(camera_socket, 'CAMERA', Cam_Dummy.camera_output())


    # sleep 
    time.sleep(0.1)
