# Import libraries
import os
import xlrd 

# Ensure code is being run in SPAM-MENU
SPAM_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(SPAM_folder)

# Import database files
from database.common_menu import *

def main():
    print("Hi this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his depression.")
    while True:
        main_menu = Menu("Leave Mall", Leave_Mall())
        choice = main_menu.show_menu()
        main_menu.options[choice].leave_mall()

main()
"""
    main_menu.add_menu( "1", "Login/Register" 
                        "2", "Get a shopping cart/basket", 
                        "3", "Explore the shopping aisle", 
                        "4", "Search for specific item", 
                        "5", "Head to the cashier")
"""