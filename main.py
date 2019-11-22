# Import stuff
import os
import getpass
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
        self.name = "Logout"
    
    def action(self):
        return True

class LoginRegister:
    def __init__(self):
        self.name = "Login/Register"
        self.users = pd.read_csv("data/users.csv")
        self.user_list = self.users['username'].unique()
    
    def update_users(self):
        self.users = pd.read_csv("data/users.csv")
        self.user_list = self.users['username'].unique()

    def login(self):
        while True:
            clear()
            print(print_banner(self.name, "Login"))
            find_user = input("Username: ")
            password = getpass.getpass("Password: ")
            if find_user in self.user_list:
                user_password = self.users.loc[self.users['username'] == find_user, 'password'].values[0]
                if password == user_password:
                    self.username = find_user
                    self.user_type = self.users.loc[self.users['username'] == self.username, 'account_type'].values[0]
                    print(f"Welcome back {self.username}!")
                    enter_to_continue()
                    return 0
            choice = yes_or_no("Invalid credentials! Go back?")
            if choice:
                return 1

    def register(self, admin = False):
        clear()
        print(print_banner(self.name, "Register"))
        user_details = [None]*3
        usernames = self.users['username'].unique()
        if admin == False:
            while True:
                print("Welcome! I see this is your first time here! Before we get into the program, please tell me a bit about yourself!\n")
                user_details[0] = input("Username: ").strip()
                if user_details[0] in usernames:
                    choice = yes_or_no("Username taken. Cancel?")
                    if choice:
                        return 1
                    else:
                        continue
                user_details[1] = getpass.getpass("Password: ")
                user_details[2] = getpass.getpass("Enter password again: ")
                if user_details[1] != user_details[2]:
                    print("Passwords do not match!")
                    enter_to_continue()
                else:
                    break
            user_details[2] = "Customer"
            clear()
            print(print_banner("Register"))
            print(f"Welcome {user_details[0]}!")
            enter_to_continue()

            # Tell main program name user details
            self.username = user_details[0]
            self.user_type = "Customer"

            # Update database
            user_details = pd.DataFrame([user_details], columns = self.users.columns)
            self.users = self.users.append(user_details, ignore_index = True)
            self.users.to_csv('data/users.csv', index=False)
            return 0

    def action(self):
        while True:
            self.update_users()
            clear()
            print(print_banner(self.name))
            choice = yes_or_no("Is this your first time here?")

            # Login or register
            if choice:
                choice = self.register()
            else:
                choice = self.login()

            # If user cancels, return 1
            if choice == 0: 
                break

# Create temp menu for cart to refer to 
stock = Stock()
stock.readStockFromOG()
# Login/Register
login = LoginRegister()

def main():
    clear()
    print_banner("Krusty Krabz")
    login.action()
    clear()

    # Different menu depending on the account type
    if login.user_type == "Customer":
        msg = f"Welcome {login.username} this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his depression."
        main_menu = Menu(msg, "0", LeaveMall())
        main_menu.add_menu("1", ExploreAisle())
        main_menu.add_menu("2", ShoppingCart())
        main_menu.add_menu("3", Checkout())
    elif login.user_type == "Admin":
        main_menu.add_menu("2", Stock())
       
    logout = False
    while logout == False:
        choice = main_menu.show_menu()
        logout = main_menu.options[choice].action()
    
    clear()
    print(print_banner("Exit"))
    choice = yes_or_no("Exit entirely?")
    if choice:
        exit(0)

clear_cart()
# Main loop
main()
clear_cart()

"""
    main_menu.add_menu( "1", "Login/Register" 
                        "2", "Get a shopping cart/basket", 
                        "3", "Explore the shopping aisle", 
                        "4", "Search for specific item", 
                        "5", "Head to the cashier")
"""