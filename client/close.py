import socket
import time

from database.sockets import Client

HOST = "localhost"
PORT = 8039
BUFF_LENGTH = 1024

client = Client(HOST, PORT)
client.send_string('180', "HAH")
client.close_conn()