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

    def close_conn(self):
        self.client.close()
    
    def send_string(self, code_num, msg):
        """Send short strings\n
        100 - Client Start\n
        101 - New User\n
        102 - Login\n
        105 - Checkout\n
        180 - Close Server"""
        self.client.send(f"{code_num}_{msg}".encode())
    
    def send_file(self, code_num, filename, BUFF_LENGTH):
        """Read the file at chunks at a time"""
        out_file = open(filename,"rb")
        file_bytes = out_file.read(1024) 
        while file_bytes != b'':
            self.client.send(file_bytes)
            file_bytes = out_file.read(1024) # read next block from file
    
    def recv_string(self, BUFF_LENGTH):
        msg = self.client.recv(BUFF_LENGTH).decode()
        if len(msg) == 0:
            msg = -1
        return msg