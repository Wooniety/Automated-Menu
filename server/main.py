# Import stuff
import os
import threading
import traceback

# Run code in SPAM-MENU
spam_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(spam_folder)

# Import database files
from database.sockets import Server

# Start the server
HOST = "localhost"
PORT = 8039
print(f"SPAM server started at {HOST} at port {PORT}")
server = Server(HOST, PORT)

def client_thread(code, BUFF_LENGTH = 4096):
    print("Connection receieved!")
    code, msg = server.recieve_string(BUFF_LENGTH)
    print(f"{code} {msg}")
    server.send_string("0")
    

while True:
    server.start_conn()
    try:
        code = 0
        threading.Thread(target=client_thread, args=(code, 4096)).start()
        if code == '180':
            server.close_conn()
            print(f"Connection closed with {server.ip}")
            break
    except:
        print("Oops! Something went wrong!")
        traceback.print_exc()
        server.close_conn()
server.close_server()

# Receive connection type
# 1) Login
# 2) Change Cart
# 3) Checkout
# dict of those functions

#print("Server stopped")