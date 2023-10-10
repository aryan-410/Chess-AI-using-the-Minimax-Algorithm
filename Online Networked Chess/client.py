import socket

class client:
    def __init__(self):
        self.HEADER = 64
        self.PORT = 5000
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "192.168.0.187"
        self.ADDR = (self.SERVER, self.PORT)
        
        self.clientConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientConn.connect(self.ADDR)
        self.connected = True

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.clientConn.send(send_length)
        self.clientConn.send(message)
        if msg == self.DISCONNECT_MESSAGE: self.connected = False
        self.recieved_message = self.clientConn.recv(2048).decode(self.FORMAT)
