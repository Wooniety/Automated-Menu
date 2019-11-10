# Import stuff
import os
import xlrd 
import pandas as pd

# Ensure code is being run in SPAM-MENU
SPAM_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(SPAM_folder)

# Import database files
from database.common_menu import *

def main():
    clear()
    msg = "Hi this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his depression.\n"
    while True:
        main_menu = Menu(msg, "0", Leave_Mall())
        main_menu.add_menu("1", Login_Register())
        choice = main_menu.show_menu()
        main_menu.options[choice].action()

main()
"""
    main_menu.add_menu( "1", "Login/Register" 
                        "2", "Get a shopping cart/basket", 
                        "3", "Explore the shopping aisle", 
                        "4", "Search for specific item", 
                        "5", "Head to the cashier")
"""