import numpy as np
import zmq
import time
import struct

# init as publisher
ZMQ_client_context = zmq.Context()
client_socket = ZMQ_client_context.socket(zmq.PUB)

#set high-water mark to 1
client_socket.setsockopt(zmq.SNDHWM, 1)
client_socket.bind("tcp://127.0.0.1:5556")

print('started server...')


def read():
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
    return values


while True:
    values = read()
    # can only send byte-like objects
    values = struct.pack('f' * len(values), *values)
    # send name, values and timestamp
    client_socket.send_multipart((b"MAXBOX", values, str(time.time()).encode()))
    # sleep for one second
    time.sleep(0.1)


