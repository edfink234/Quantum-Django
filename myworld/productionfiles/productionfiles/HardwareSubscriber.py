from channels.layers import get_channel_layer
import zmq
import struct
import asyncio
from multiprocessing import Process


class HardwareSubscriber:
    """
    The Hardware Subscriber handles the subscriptions to the hardware publishers.
    Examples for hardware publishers are the camera, PMT count, photodiodes, etc.
    They publish their data via ZMQ PUB sockets, the data is received with ZMQ SUB sockets.
    It is then sent to the channel layer to be displayed on the GUI.
    """

    def __init__(self, sub_socket, channel_layer, address, names, return_types):

        # get address
        self.address = address

        # get names
        self.names = names

        # get return types
        self.return_types = return_types

        # get SUB socket
        self.sub_socket = sub_socket

        # get channel layer for communication with GUI
        self.channel_layer = channel_layer

        # connect the Hardware Subscriber to the PUB sockets
        self.sub_socket.connect(address)
        # subscribe to all names of this socket
        for name in self.names:
            self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, name)


    async def listen(self):
        """
        Receive and process data from the publishers, then send it to channel layer.
        """

        # listen continuously
        while True:
            try:
                # TODO: is it fast enough to do it all in one thread or should this be multithreaded/multiprocessed?
                
                # receive topic, message and time from the socket
                [topic, message, time] = self.sub_socket.recv_multipart()

                topic = topic.decode()
                time = time.decode()
                return_type = self.return_types[topic]

                # depending on which return type the data has, it needs to be decoded in a different way
                if return_type == 'float':
                    decoded_message = struct.unpack('!f', message)[0]

                elif return_type == 'list':
                    num_floats = len(message) // struct.calcsize('f')
                    decoded_message = list(struct.unpack('f' * num_floats, message))

                elif return_type == 'int':
                    decoded_message = struct.unpack('!i', message)[0]

                elif return_type == 'string' or return_type == 'str':
                    decoded_message = message.decode('utf-8')

                else:
                    print('WARNING: UNKNOWN RETURN TYPE')
                    try: 
                        decoded_message = message.decode('utf-8')
                    except:
                        print('MESSAGE CANNOT BE DECODED')
                # send data to channel layer
                data = [topic, decoded_message, time]
                await self.channel_layer.group_send("ZMQ",{"type": "chat.message", "text": data}) # TODO: is it possible to send the messages without converting to string?
            
            # zmq.Again is typically raised when a non-blocking operation cannot be completed immediately and needs to be retried later
            except zmq.Again:
                continue

async def main(task_list):
    await asyncio.gather(*task_list)


if __name__ == '__main__':

    print('Started Hardware Subscriber...')
    # Subscription list: list with dictionary containing name, address, return type of subscription
    subs = [
            {'name':'MAXBOX',       'address':'tcp://localhost:5556', 'return type': 'list'},
            {'name':'TEMPERATURE',  'address':'tcp://localhost:5557', 'return type': 'float'},
            {'name':'PRESSURE',     'address':'tcp://localhost:5557', 'return type': 'float'},
            {'name':'CAMERA',       'address':'tcp://localhost:5558', 'return type': 'list'}]
    
    # get list of addresses (duplicates are allowed but should only appear once in this list)
    addresses = list(set(sub['address'] for sub in subs))

    # get dictionary with address as key and list of names as value
    names = {sub['address']: [] for sub in subs}
    for sub in subs:
        names[sub['address']].append(sub['name'])

    # get dictionary with name as key and return type as value
    return_types = {sub['name']: sub['return type'] for sub in subs}
    
    # Create a SUB socket
    context = zmq.Context()
    sub_socket = context.socket(zmq.SUB)

    # get channel layer for communication with GUI
    channel_layer = get_channel_layer()

    # create instances for each subscription
    HaSubs = [HardwareSubscriber(sub_socket, channel_layer, address, names[address], return_types) for address in addresses]
    
    # run all subscriptions with asyncio
    asyncio.run(main([HaSub.listen() for HaSub in HaSubs]))
