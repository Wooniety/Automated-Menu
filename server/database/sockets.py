# Stuff I actually need
import sys
import socket
import threading

class Server:
    def __init__(self, host, port, no_conns = 5):
        """Start the server and listen"""
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.server.bind((host, port))
        except socket.error:
            print('Bind failed. Error : ' + str(sys.exc_info()))
            sys.exit()
        self.server.listen(no_conns)
        print("Listening...")

    def start_conn(self):
        self.conn, self.addr = self.server.accept()
        self.ip = str(self.addr[0])
        self.port = str(self.addr[1])

    def close_conn(self):
        self.conn.close()
    
    def recieve_string(self, BUFF_LENGTH):
        """On existing connection, recieve string\n
        NUM_MSG - 100_serverstuff
        returns code num and string"""
        buf = self.conn.recv(BUFF_LENGTH)
        buf = buf.decode()
        if len(buf) == 0:
            buf = -1
        return buf[:3], buf[4:] # 100, msg
    
    def recv_file(self, filename, BUFF_LENGTH, min_len = 0):
        file_bytes = b''
        while True:
            file_bytes += self.conn.recv(BUFF_LENGTH)
            if len(file_bytes) > 0:
                break
        if len(file_bytes) > min_len:
            in_file = open(filename,"wb")
            in_file.write(file_bytes)
            in_file.close()

    def send_string(self, msg):
        """send(string)"""
        msg_bytes = msg.encode()
        self.conn.send(msg_bytes)

    def send_file(self, filename, BUFF_LENGTH):
        """Read the file at chunks at a time"""
        out_file = open(filename,"rb")
        file_bytes = out_file.read(1024) 
        while file_bytes != b'':
            self.conn.send(file_bytes)
            file_bytes = out_file.read(1024) # read next block from file
        self.conn.send(b'')

    def close_server(self):
        self.server.close()
    
    # TODO function to change server host, port and no_conns