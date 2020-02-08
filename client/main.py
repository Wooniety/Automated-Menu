# Import stuff
import os
import time
import pandas as pd
import socket

# Ensure code is being run in SPAM-MENU
spam_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(spam_folder)

# Import database files
from database.utils import *
from database.common_menu import *
from database.stock import *
from database.admin_functions import *
from database.shopping import *
from database.sockets import Client

HOST = "localhost"
PORT = 8039
BUFF_LENGTH = 1024

# Leave Mall
class LeaveMall:
    def __init__(self):
        self.name = "Logout"
    
    def action(self):
        return True

# Create temp menu for cart to refer to 
stock = Stock()
stock.readStockFromOG()

login = LoginRegister()

# Main Loop
def main():
    clear_cart()
    clear()
    print_banner("Krusty Krabz")
    while True:
        choice = login.action()
        client = Client(HOST, PORT)
        if choice == 0:
            client.send_string('101', f"{login.username}/{login.password}/{login.user_type}")
            break
        elif choice == 1:
            # Verify user
            client.send_string('102', f"{login.username}/{login.password}")
            check = client.recv_string(BUFF_LENGTH)
            if check == '-1':
                print("Invalid credentials!")
            else:
                login.user_type = check
                break
        client.close_conn()
        enter_to_continue()
    clear()

    # Get the menu of the day
    client = Client(HOST, PORT)
    client.send_string("111", get_day().lower())
    client.recv_file('data/day_items.csv', BUFF_LENGTH)
    client.close_conn()

    # Different menu depending on the account type
    if login.user_type == "Customer":
        customer_menu = (ExploreAisle(), SearchItem(), ShoppingCart(), Checkout())
        msg = f"Welcome {login.username} this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his sadness."
        main_menu = Menu(msg, "0", LeaveMall())
        for i, option in enumerate(customer_menu):
            main_menu.add_menu(f"{i+1}", option)
    elif login.user_type == "Admin":
        client = Client(HOST, PORT)
        client.send_string("112", 'users.csv')
        client.recv_file('data/users.csv', BUFF_LENGTH)
        client.close_conn()
        admin_menu = (CheckUsers(login.username, Client(HOST, PORT)), ChangeStock(Client(HOST, PORT)))
        msg = f"Welcome back boss..."
        main_menu = Menu(msg, "0", LeaveMall())
        for i, option in enumerate(admin_menu):
            main_menu.add_menu(f"{i+1}", option)
       
    # Send server request for 
    logout = False
    while logout == False:
        choice = main_menu.show_menu()
        logout = main_menu.options[choice].action()

    # Send server back all the things
    client = Client(HOST, PORT)
    if login.user_type == 'Customer':
        client.send_string('105', f"{login.username}_{get_time()}")
        time.sleep(1)
        client.send_file('data/cart.csv', BUFF_LENGTH)
    client.close_conn()

    clear_cart()
    clear()

    print(print_banner("Exit"))
    choice = yes_or_no("Exit completely?")
    if choice:
        exit(0)

clear()

# Main loop
while True:
    main()