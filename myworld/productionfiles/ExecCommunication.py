import json
import logging
import time
from typing import Optional, Union
import uuid
import pathlib

from channels.layers import get_channel_layer


logger = logging.getLogger(__name__)

# from RPC_server.backend.hermione_server import hermione_server
from transport_layer_zmq.basics.authentication import ClientAuthentication
from transport_layer_zmq.architecture.hermione.common import TargetNotAvailableException
from transport_layer_zmq.architecture.hermione.client_device import ClientDevice
from transport_layer_zmq.test.testing_tools import get_keys

class ExecCommunication:
    """
    ExecCommunication handles the communication to the Execution Controller.
    It parses the requests to the right format and sends it via the Software Handler Switch to the Execution Controller.
    """

    def __init__(self):
        # TODO: change init variables to be read from env file
        # KEYPATH 
        path = "switchkey/env-network-transport-layer-both.txt"

        pub_key, _ = get_keys(pathlib.PurePath(path))
        self.client_auth = ClientAuthentication(pub_key)
        # address of the switch
        self.addr = "tcp://127.0.0.1:52021"
        self.name = b"ExecCommunication"
        self.pw = b""

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
            result = json.loads(result)
            if "result" in result:
                return result["result"]
            elif "error" in result:
                print('An error occurred:', result["error"])
                return result["error"]
            
    def send_request(self, method, params):
        with ClientDevice(self.addr, self.client_auth, self.name, self.pw, None) as dev:

            reply = self.blocking_rpc(dev, b"ExecConDummy", method, params)
            if reply is None:
                print("No reply came from ExecConDummy in time - you could retry later")
            print('Reply from ExecCon:', reply)
            
    def set_values(self, params):
        """
        Direct mode communication

        Parameters
        ----------
        params : list
            first entry define which value to set, following entries define the parameters for that value
        """
        method = 'ExecConD.set_values'
        self.send_request(method, params)

    def exec_exp(self,params):
        """
        Execute Experiment communication

        Parameters
        ----------
        params : list
            first entry define which experiment to execute, following entries define the parameters for that experiment
        """
        method = 'ExecConD.exec_exp'
        self.send_request(method, params)

    def test(self, message):
        """
        For testing the connection to the Execution Controller

        Parameters
        ----------
        message : string
            test string, can be any string
        """
        print('test message:', message)
        method, params = 'ExecConD.test', [message]
        self.send_request(method, params)


if __name__ == '__main__':
    ExecComm = ExecCommunication()
    ExecComm.test('this is a test')
    ExecComm.set_values(['setXYZ', 420])
    ExecComm.exec_exp(['myCoolExperiment', True, 20])