# Import stuff
import os

# Run code in SPAM-MENU
spam_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(spam_folder)

# Import database files
from database.sockets import Server
from database.common_menu import Menu

# Start the server
Server('0.0.0.0', 8039)
Server.start_conn
print("SPAM server started on ")

main()

# Receive connection type
# 1) Login
# 2) Change Cart
# 3) Checkout

Server.close_conn
print("Server stopped")