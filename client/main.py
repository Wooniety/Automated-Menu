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
from database.shopping import *
from database.sockets import Client

HOST = "localhost"
PORT = 8039
BUFF_LENGTH = 1024

class ChangeStock:
    def __init__(self, socket):
        self.socket = socket
        self.name = "Modify Stock"
        self.stock = Stock()
 
    def viewStock(self):
        """Shows all the stocks"""
        self.stock.updateStockDF()
        clear()
        print(print_banner(self.name, "View Stock"))
        print("All the items in the store:")
        self.stock.showAll()

    def restock(self):
        """Add quantity to items"""
        while True:
            self.stock.updateStockDF()
            clear()
            print(print_banner(self.name, "Add Stock"))
            stock_list = self.stock.stock_df.values # [[Item, Category, Price, Quantity]]
            item_dict = {}
            # Add items to a dictionary for easy reference
            for i, item in enumerate(stock_list):
                item_dict[f"{i+1}"] = [item[0], item[1], item[2], item[3]]
            display_stock = self.stock.stock_df
            display_stock.index += 1
            print(display_stock)
            while True:
                clear()
                print(print_banner(self.name, "Add Stock"))
                print(display_stock)
                choice = input("\nPick an item to add (0 to quit): ").strip()
                if choice == "0": # Stop restocking
                    return 
                if valid_option(choice, len(item_dict)) == False:
                    print("Invalid option!")
                    enter_to_continue()
                    continue
                item_name = item_dict[choice][0].capitalize()
                amt = input(f"How many {item_name}: ")
                if amt.isnumeric() == False:
                    print("Invalid option!")
                    enter_to_continue()
                    continue
                item_dict[choice][3] = int(amt)
                self.stock.addStock([item_dict[choice]])
                break
            print(f"{amt} {item_name} added")
            enter_to_continue()
 
    def addItem(self):
        """Add new item to stock"""
        while True:
            self.stock.updateStockDF()
            clear()
            print(print_banner(self.name, "Add Item to Stock"))
            item_to_add = [None]*4
            prompts = ["Item name: ", "Category: ", "Price: ", "Stock: "]
            print(self.stock.stock_df.to_string(index = False))
            print("\nJust need you to fill in some details to add a new item... (0 to quit)")
            for i, prompt in enumerate(prompts):
                item_to_add[i] = input(prompt).strip()
                if i < 2:
                    if item_to_add[i] == "0":
                        return
                    while True:
                        if item_to_add[i] == "":
                            item_to_add[i] = input(prompt).strip()
                        else:
                            break
                    item_to_add[i] = item_to_add[i].lower().capitalize()
                else:
                    while True:
                        if if_num(item_to_add[i]) == False:
                            item_to_add[i] = input(prompt).strip()
                        else:
                            break
                    item_to_add[i] = float(item_to_add[i])

            if item_to_add[0] in self.stock.all_items:
                print("Item already exists!")
                continue
            # Add {num} {item name} in the {category} for {price} each? 
            choice = yes_or_no(f"Add {item_to_add[3]} {item_to_add[0]} in the {item_to_add[1]} for ${to_num(item_to_add[2], '', True, 2)} each?")

            if choice:
                print(f"Added {item_to_add[0]}")
                item_to_add = pd.DataFrame([item_to_add], columns = self.stock.stock_df.columns)
                self.stock.stock_df = self.stock.stock_df.append(item_to_add, ignore_index = True)
                self.stock.updateStockCSV()
                self.stock.updateActualStockCSV()
            else:
                print("Cancelled")
            enter_to_continue()

    def removeStock(self):
        while True:
            self.stock.updateStockDF()
            all_items = self.stock.all_items
            clear()
            print(print_banner(self.name, "Remove Item"))
            print(self.stock.stock_df.to_string(index = False))
            item_to_remove = input("Enter the name of the item to be removed (0 to exit): ").strip().lower()
            if item_to_remove == "0":
                break
            for item in all_items:
                if item_to_remove == item.lower():
                    choice = yes_or_no(f"Remove {item}?")
                    if choice:
                        self.stock.removeStock(item, self.stock.getCell(item, "Stock"))
                        self.stock.updateActualStockCSV()
                        print(f"Removed {item}")
                        enter_to_continue()
                    else:
                        break
            else:
                print("Item does not exist!")

    def action(self):
        self.stock.updateStockDF()
        menu = MenuFunctions("View Stock", self.viewStock, "Restock",  self.restock, "Add Item", self.addItem, "Remove Stock", self.removeStock)
        menu.show_functions(self.name)
        self.stock.updateActualStockCSV()
        return False

class CheckUsers:
    def __init__(self, current_user, socket):
        self.socket = socket
        self.current_user = current_user
        self.name = "Check Users"
        self.login_stuff = LoginRegister()
        self.login_stuff.getUsers()
        self.users = self.login_stuff.users
        self.users.index += 1
        self.stock = Stock() 

    def viewAllUsers(self, show_index = True):
        print((self.users[['Username','account_type']]).to_string(index = show_index))
        enter_to_continue()
    
    def addAdmin(self):
        self.login_stuff.register(True)
    
    def removeUser(self):
        while True:
            clear()
            print(print_banner(self.name, "Remove User"))
            self.viewAllUsers(False)
            user_remove = input("Enter name of user to remove (0 to cancel): ").strip().lower()
            client = Client(self.HOST, self.PORT)
            client.send_string("130", user_remove)
            client.close_conn()
            # FIXME send remove to server
            print(f"{user_remove} removed.")
            enter_to_continue()
    
    def action(self):
        menu = MenuFunctions("View all users", self.viewAllUsers, "Add admin", self.addAdmin, "Remove user", self.removeUser)
        menu.show_functions(self.name)
        return False

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
        admin_menu = (CheckUsers(login.username), ChangeStock())
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