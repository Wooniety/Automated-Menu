# Import stuff
import os
import pandas as pd

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
        msg = f"Welcome {login.username} this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his sadness."
        main_menu = Menu(msg, "0", LeaveMall())
        main_menu.add_menu("1", ExploreAisle())
        main_menu.add_menu("2", SearchItem())
        main_menu.add_menu("3", ShoppingCart())
        main_menu.add_menu("4", Checkout())
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

# Main loop
while True:
    main()