import logging
from typing import Optional

from .common import CommonBackend
from transport_layer_zmq.architecture.hermione.device import Device, Message
from transport_layer_zmq.basics.authentication import ClientAuthentication

class hermione_server(CommonBackend):
    def init(self, address: str, public_key: str, log_level: Optional[int] = None):
        """
        Initialization of a hermione device.

        Parameters
        ----------
        address : str
            has the format: tcp://xxx.xxx.xxx.xxx:port
        public_key : str
            string path to puplic key file of the hardware handler.
        log_level : Optional[int], optional
            Log level for device logging. None means to use internal default. Default value is None.
        """

        auth = ClientAuthentication(public_key)
        self.dev = Device(address, auth, log_level=log_level)
        self.logger = logging.Logger("RPCServerLogger", level=log_level)
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)

    def serve(self, name: str, pw: Optional[bytes] = None):
        """
        Start the rpc client under given name.

        Parameters
        ----------
        name : str
            Name of the device.
        pw : Optional[bytes], optional
            Password used for authentication.
            None to not set an password. Default is None.
        """

        self.dev.automatic_reply_loop(name.encode(), pw, self.handle_message)

    def handle_message(self, msg: Message) -> Message:
        """
        Wrapper for handling messages. Allows to simply adapt to hermione Device
        function changes and enables easy logging access.

        Parameters
        ----------
        msg : Message
            The request message as received by the hermione Device.

        Returns
        -------
        Message
            The reply message to send (back).
        """

        self.logger.debug("Received request message: %s", msg)
        request_payload = msg.get_request_str()
        self.logger.log(15, "Payload of request: %s", request_payload)
        reply_payload = self.manager.get_payload_for_payload(request_payload)
        self.logger.log(15, "Payload for reply: %s", reply_payload)
        reply_msg = msg.reply(reply_payload.encode())
        self.logger.debug("Reply message: %s", reply_msg)

        return reply_msg
