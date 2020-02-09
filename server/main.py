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

while True:
    server.start_conn()
    try:
        threading.Thread(target=server.start_thread).start()
    except:
        print("Oops! Something went wrong!")
        #traceback.print_exc()
        server.close_conn

# Receive connection type
# 1) Login
# 2) Change Cart
# 3) Checkout
# dict of those functions

Server.close_conn
#print("Server stopped")