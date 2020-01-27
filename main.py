# Import stuff
import os
import pandas as pd
import socket
import ssl

# Ensure code is being run in SPAM-MENU
spam_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(spam_folder)

# Import database files
from database.utils import *
from database.common_menu import *
from database.stock import *
from database.shopping import *
from database.admin_functions import *

# Leave Mall
class LeaveMall:
    def __init__(self):
        self.name = "Logout"
    
    def action(self):
        return True

# Create temp menu for cart to refer to 
stock = Stock()
stock.readStockFromOG()
# Login/Register
login = LoginRegister()

def main():
    clear_cart()
    clear()
    print_banner("Krusty Krabz")
    login.action()
    clear()
    

    # Different menu depending on the account type
    if login.user_type == "Customer":
        customer_menu = [ExploreAisle(), SearchItem(), ShoppingCart(), Checkout()]
        msg = f"Welcome {login.username} this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his sadness."
        main_menu = Menu(msg, "0", LeaveMall())
        for i, option in enumerate(customer_menu):
            main_menu.add_menu(f"{i+1}", option)
    elif login.user_type == "Admin":
        msg = f"Welcome back boss..."
        main_menu = Menu(msg, "0", LeaveMall())
        main_menu.add_menu("1", CheckUsers(login.username))
        main_menu.add_menu("2", ChangeStock())
       
    logout = False
    while logout == False:
        choice = main_menu.show_menu()
        logout = main_menu.options[choice].action()
    
    clear()
    print(print_banner("Exit"))
    choice = yes_or_no("Exit completely?")
    if choice:
        exit(0)
    clear_cart()

# Connect to server
"""
host_addr = '0.0.0.0'
host_port = 8000
server_sni_hostname = 'example.com'
server_cert = 'server.crt'
client_cert = 'client.crt'
client_key = 'client.key'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print("SSL established. Peer: {}".format(conn.getpeercert()))
conn.send(b"Hello, world!")
conn.close()
"""

clear()

# Main loop
while True:
    main()