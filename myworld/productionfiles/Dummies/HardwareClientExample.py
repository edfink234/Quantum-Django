import zmq
import struct
import datetime

context = zmq.Context()

# Create a SUB socket
sub_socket = context.socket(zmq.SUB)

# Connect to maxbox PUB socket
sub_socket.connect("tcp://localhost:5556")

# Connect weather PUB socket
sub_socket.connect("tcp://localhost:5557")

# Connect camera PUB socket
sub_socket.connect("tcp://localhost:5558")

# Set the subscription filter for specific topics
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "MAXBOX")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "TEMPERATURE")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "PRESSURE")
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "CAMERA")

# Receive and process messages
while True:
    [topic, message, time] = sub_socket.recv_multipart()
    print("Received message for topic:", topic.decode())

    if topic.decode() in ["TEMPERATURE", "PRESSURE"] : 
        print("Message:", struct.unpack('!f', message)[0])
    elif topic.decode() in ["MAXBOX", "CAMERA"] : 
        num_floats = len(message) // struct.calcsize('f')
        print("Message:", struct.unpack('f' * num_floats, message))
    else :
        print("UNKNOWN TOPIC")

    dt_object = datetime.datetime.fromtimestamp(float(time.decode()))
    time_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    print("Time: ", time_string)
    print('')
