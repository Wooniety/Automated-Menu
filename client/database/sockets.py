import socket
import threading

#TODO secure the connection. Maybe SSL tunneling

class Client:
    """Start Client"""
    def __init__(self, host, port):
        self.client = socket.socket()
        self.host = host
        self.port = port
        self.client.connect((self.host, self.port))
    
    def start_conn(self):
        self.client.connect((self.host, self.port))

    def close_conn(self):
        self.client.close()
    
    def send_string(self, code_num, msg):
        """Send short strings\n
        101 - New User\n
        102 - Login\n
        105 - Checkout\n
        111 - Get Daily Menu\n
        112 - Get File\n
        120 - Send File\n
        180 - Close Server"""
        self.client.send(f"{code_num}_{msg}".encode())
    
    def send_file(self, filename, BUFF_LENGTH):
        """Read the file at chunks at a time"""
        out_file = open(filename,"rb")
        file_bytes = out_file.read(1024) 
        while file_bytes != b'':
            self.client.send(file_bytes)
            file_bytes = out_file.read(1024) # read next block from file
        self.client.send(b'')
    
    def recv_file(self, filename, BUFF_LENGTH):
        in_file = open(filename,"wb")
        file_bytes = b''
        while True:
            file_bytes += self.client.recv(BUFF_LENGTH)
            if len(file_bytes) > 0:
                break
        in_file.write(file_bytes)
    
    def recv_string(self, BUFF_LENGTH):
        msg = self.client.recv(BUFF_LENGTH).decode()
        if len(msg) == 0:
            msg = -1
        return msg