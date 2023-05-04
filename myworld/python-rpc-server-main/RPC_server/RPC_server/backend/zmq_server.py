from .common import CommonBackend
import zmq

class zmq_server(CommonBackend):

    def init(self, address):
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind(address)


    def serve(self):
        while True:
            message = self.socket.recv_string()
            response = self.manager.get_payload_for_payload(message)
            self.socket.send_string(response)