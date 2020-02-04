import socket
import threading

#TODO secure the connection. Maybe SSL tunneling

class Server:
    def __init__(self, host, port, no_conns = 5):
        """Start the server and listen"""
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(no_conns)
    
    def start_conn(self):
        self.conn, self.addr = self.server.accept()
        # Threading shld go here?
    
    def close_conn(self):
        self.conn.close()
    
    def recieve(self, buff_length):
        """On existing connection, recieve string"""
        buf = self.conn.recv(buff_length)
        return buf.decode()

    def send(self, msg):
        """send(string)"""
        msg_bytes = msg.encode()
        self.conn.sendall(msg_bytes)

    def close_server(self):
        self.server.close()
    
    # TODO function to change server host, port and no_conns