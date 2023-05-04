import numpy as np

from RPC_server.backend.zmq_server import zmq_server

#initialize the rpc server

api = zmq_server()
api.init("tcp://127.0.0.1:5556")

print('started rpc server...')


@api.add_function
def read():
    """
    Returns an array of all values with the newest read voltages.
    Keep in mind that it takes 500ms for a full read cycle of all channels.

    Returns
    -------
    array
        voltages read from the sensor
    """

    values = np.random.rand(16).tolist()
    return values


@api.add_function
def rpc_info():
    return api.rpc_info()
    
api.serve()

