import socket
import threading

#TODO secure the connection. Maybe SSL tunneling

class Client:
    def __init__(self):
        self.client = socket.socket()
    
    def start_conn(self, host, port):
        """start_conn('0.0.0.0', 8089)"""
        self.client.connect((host, port))

    def close_conn(self):
        self.client.close()
    
    def send_string(self, msg):
        """send(str)"""
        self.client.send(msg.encode())
    
    def recv_string(self, buf):
        pass

    def send_file(self, filename, buf):
        f = open(filename, "rb")
        l = f.read(buf)
        while (l):
            self.client.send(l)
            l = f.read(buf)