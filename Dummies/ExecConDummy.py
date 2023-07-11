from RPC_server.backend.hermione_server import hermione_server
import logging
import time
from typing import Optional, Union
import uuid
import pathlib
import json

# logging
logger = logging.getLogger(__name__)

# from RPC_server.backend.hermione_server import hermione_server
from transport_layer_zmq.basics.authentication import ClientAuthentication
from transport_layer_zmq.architecture.hermione.common import TargetNotAvailableException
from transport_layer_zmq.architecture.hermione.client_device import ClientDevice
from transport_layer_zmq.test.testing_tools import get_keys

class ExecConDummy:

    def __init__(self):
        pass
    
    def to_json_rpc_request(self, method : str, params : Optional[Union[list, dict]], id : Optional[Union[str, int]] = None) -> str:
        if id is None:
            id = str(uuid.uuid4())
        
        if params is not None:
            return json.dumps({"jsonrpc": "2.0", "id": id, "method": method, "params": params})
        else:
            return json.dumps({"jsonrpc": "2.0", "id": id, "method": method})

    def send_recv_msg_blocking(self, dev : ClientDevice, target : bytes, msg : str, timeout : float) -> Optional[str]:
        logger.debug("Sending message %s to %s.", msg, target)
        print("Sending message", msg ,"to", target)
        
        msg_id = dev.send_request_string(msg, target)
        
        logger.debug("Waiting for response...")
        
        start_time = time.time()
        received = None
        while received is None:
            try:
                received = dev.recv_reply_string(timeout / 5, msg_id)
            except TargetNotAvailableException:
                logger.error("Could not connect to target %s.", target)
                return None
            
            if time.time() - start_time > timeout:
                # timeout
                print('timeout')
                logger.warning("Did not receive response from %s in timeout time of %ss. Returning None.", target, timeout)
                return None
        
        logger.info("Received reply %s for blocking request %s.", received, msg)
        return received

    def blocking_rpc(self, dev:ClientDevice, target:bytes, method:str, params:Optional[Union[list, dict]], id:Optional[Union[str, int]]=None, timeout:float=5.0):
        msg = self.to_json_rpc_request(method, params, id)
        result = self.send_recv_msg_blocking(dev, target, msg, timeout)
        if result is not None:
            print('result:',result)
            result = json.loads(result)
            if "result" in result:
                return result["result"]
            elif "error" in result:
                print('An error occurred:', result["error"])
                return result["error"]




    def set_values(self, func_name, *args, **kwargs):
        print('Setting', func_name, 'to', args, kwargs)
        if func_name == 'BerthaSetDigital':
            # KEYPATH - use custom keypath if you run this script
            path = "C:/Users/wpauline/switchkey/env-network-transport-layer-both.txt"

            # authentification
            pub_key, _ = get_keys(pathlib.PurePath(path))
            client_auth = ClientAuthentication(pub_key)
            # address of the switch
            addr = "tcp://127.0.0.1:52021"
            # name for registration at the switch
            name = b"HardwareHandler"
            pw = b""

            with ClientDevice(address=addr, authentication=client_auth, name=name, pw=pw, auto_request_handling_func=None, router_address="tcp://127.0.0.1:51242") as dev:

                method, params = 'BerthaP.set_digital', {"value": int(args[0])} # yellow channel 0, green channel 2
                print('setting Bertha digital channels to', args[0])

                # send request to BerthaProcess, get reply
                reply = self.blocking_rpc(dev, b"BerthaProcess", method, params)
                if reply is None:
                    print("No reply came from Bertha in time - you could retry later")
                print('Reply from Bertha:', reply)
        return True

    def exec_exp(self, exp_name, *args, **kwargs):
        print('Executing', exp_name, 'with parameters', args, kwargs)
        return True

    def test(self, message):
        print('test message:', message)
        return True



def main():

    #switch_address = 'tcp://host.docker.internal:52021'
    switch_address = 'tcp://127.0.0.1:52021'
    alt_keypath = '../myworld/switchkey/env-network-transport-layer.txt'


    api = hermione_server()

    try: # when run from repository
        keypath = 'switch_key.key'
        print('getting keys from', keypath)
        api.init(switch_address, keypath, log_level=logging.INFO)

    except: # when run locally
        print('failed...')
        keypath = alt_keypath
        print('getting keys from', keypath)
        api.init(switch_address, keypath, log_level=logging.INFO)

    ExecConD = ExecConDummy()
    api.add_object(ExecConD, 'ExecConD') # address functions with ExecConD.function_name
    api.serve('ExecConDummy') # registration name for switch; use this string as the target parameter in the client when sending a request


if __name__ == '__main__':
    main()