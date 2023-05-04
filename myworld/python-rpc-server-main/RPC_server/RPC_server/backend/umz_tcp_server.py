from .common import CommonBackend
import selectors
import socket

class umz_server(CommonBackend):
    
    def init(self, address, port):
        self.sel = selectors.DefaultSelector()
        sock = socket.socket()
        sock.bind((address, port))
        sock.listen(100)
        sock.setblocking(False)
        self.sel.register(sock, selectors.EVENT_READ, self.accept)

    def accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(4) #has to match MCP TCPClient msgLengthStringChars
        size = int.from_bytes(data, byteorder='big')
        data = conn.recv(size)

        if data:
            response = self.manager.get_payload_for_payload(data)
            mlength = str(len(response)).zfill(4)
            conn.sendall(mlength.encode("utf-8") + response.encode('utf-8'))
        else:
            self.sel.unregister(conn)
            conn.close()


    def serve(self):
        while True:
            try:
                events = self.sel.select()
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
            except ConnectionResetError:
                pass
                
