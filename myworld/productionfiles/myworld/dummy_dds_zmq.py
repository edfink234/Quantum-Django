import numpy as np

from RPC_server.backend.zmq_server import zmq_server

#initialize the rpc server

api = zmq_server()
api.init("tcp://127.0.0.1:5559")

print('started rpc server...')

@api.add_function
def set_output(freq: float, ampl: float, channel: int, phase: float = 0, profile: int = 0):
    """
    Sets frequency, amplitude and phase to output of DDS board

    Parameters
    ----------
    f: float
       frequency (Hz)
    ampl: float
       amplitude (0-1)
    channel: int
       channel (0-3)
    profile: int
       profile of channel (0-7)

    Returns
    -------
    bool
        True if successful, False otherwise.
    """
    print('setting output')
    try:
        output = 'frequency: ' + str(freq) + '\namplitude: ' + str(ampl) + '\nchannel: ' +str(channel) + '\nphase: '+ str(phase) + '\nprofile: ' + str(profile)
        with open('test_output.txt', 'w') as f:
            f.write(output)
        return True
    except Exception as e:
        print(e)
        return False
    

@api.add_function
def read_temperature(channel: int):
    """
    Reads temperature of amplifier.

    Parameters
    ----------
    channel: int
       channel (0-3)

    Returns
    -------
    float
        Temperature of the requested amplifier channel
    """
    print('reading temperature')
    temperatures = [20.0, 22.8, 19.5, 48.7]
    try:
        return temperatures[channel]
    except Exception as e:
        print(e)
        return str(e)



@api.add_function
def rpc_info():
    return api.rpc_info()

api.serve()
