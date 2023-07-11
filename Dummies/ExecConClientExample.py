import json
import logging
import time
from typing import Optional, Union
import uuid
import pathlib


logger = logging.getLogger(__name__)

# from RPC_server.backend.hermione_server import hermione_server
from transport_layer_zmq.basics.authentication import ClientAuthentication
from transport_layer_zmq.architecture.hermione.common import TargetNotAvailableException
from transport_layer_zmq.architecture.hermione.client_device import ClientDevice
from transport_layer_zmq.test.testing_tools import get_keys

def to_json_rpc_request(method : str, params : Optional[Union[list, dict]], id : Optional[Union[str, int]] = None) -> str:
    if id is None:
        id = str(uuid.uuid4())
    
    if params is not None:
        return json.dumps({"jsonrpc": "2.0", "id": id, "method": method, "params": params})
    else:
        return json.dumps({"jsonrpc": "2.0", "id": id, "method": method})

def send_recv_msg_blocking(dev : ClientDevice, target : bytes, msg : str, timeout : float) -> Optional[str]:
    logger.debug("Sending message %s to %s.", msg, target)
    
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
            logger.warning("Did not receive response from %s in timeout time of %ss. Returning None.", target, timeout)
            return None
    
    logger.info("Received reply %s for blocking request %s.", received, msg)
    
    return received

def blocking_rpc(dev:ClientDevice, target:bytes, method:str, params:Optional[Union[list, dict]], id:Optional[Union[str, int]]=None, timeout:float=5.0):
    msg = to_json_rpc_request(method, params, id)
    result = send_recv_msg_blocking(dev, target, msg, timeout)
    if result is not None:
        #print('result:',result)
        result = json.loads(result)
        if "result" in result:
            return result["result"]
        elif "error" in result:
            print('An error occurred:', result["error"])
            return result["error"]

# KEYPATH
path = "../../ExecConClient.txt"
#"C:/Users/wpauline/switchkey/env-network-transport-layer-both.txt"
    

pub_key, _ = get_keys(pathlib.PurePath(path))
client_auth = ClientAuthentication(pub_key)
# address of the switch
addr = "tcp://127.0.0.1:52021"
name = b"ExecConClient"
pw = b""

with ClientDevice(address=addr, authentication=client_auth, name=name, pw=pw, auto_request_handling_func=None, router_address="tcp://127.0.0.1:51249") as dev:

    #method, params = 'ExecConD.set_values', ['set_voltage', 'some', 'more', 'parameters']
    method, params = 'ExecConD.exec_exp', {'exp_name':'729spectroscopy', 'step':15}

    reply = blocking_rpc(dev, b"ExecConDummy", method, params)
    if reply is None:
        print("No reply came from ExecConDummy in time - you could retry later")
    print('Reply from ExecCon:', reply)
