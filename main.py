# Import stuff
import os
import pandas as pd

# Ensure code is being run in SPAM-MENU
SPAM_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(SPAM_folder)

# Import database files
from database.utils import *
from database.common_menu import *
from database.stock import *
from database.shopping import *

# Default Menu options
class LeaveMall:
    def __init__(self):
        self.name = "Leave Mall"
    
    def action(self):
        clear()
        exit(0)

class LoginRegister: #Not in use yet
    def __init__(self):
        self.name = "Login/Register"
        self.username = "User"
        self.password = "Password"
    
    def action(self):
        clear()
        exit(0)

def main():
    clear()
    msg = "Hi this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his depression."
    main_menu = Menu(msg, "0", LeaveMall())
    main_menu.add_menu("1", LoginRegister())
    main_menu.add_menu("2", Stock())
    main_menu.add_menu("3", ExploreAisle())
    main_menu.add_menu("4", ShoppingCart())
    while True:
        choice = main_menu.show_menu()
        main_menu.options[choice].action()

# Main loop
main()
"""
    main_menu.add_menu( "1", "Login/Register" 
                        "2", "Get a shopping cart/basket", 
                        "3", "Explore the shopping aisle", 
                        "4", "Search for specific item", 
                        "5", "Head to the cashier")
"""