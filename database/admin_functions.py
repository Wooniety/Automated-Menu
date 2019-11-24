# Import stuff
import pandas as pd
from database.utils import *
from database.common_menu import *
from database.stock import *

class ChangeStock:
    def __init__(self):
        self.name = "Modify Stock"
        self.stock = Stock()
    
    def viewStock(self):
        self.stock.updateStockDF()
        clear()
        print(print_banner(self.name, "View Stock"))
        print("All the items in the store:")
        self.stock.showAll()

    def restock(self):
        """Add quantity to items"""
        self.stock.updateStockDF()
        clear()
        print(print_banner(self.name, "Add Stock"))
        stock_list = self.stock.stock_df.values # [[Item, Category, Price, Quantity]]
        item_dict = {}
        for i, item in enumerate(stock_list):
            item_dict[f"{i+1}"] = [item[0], item[1], item[2], item[3]]
        display_stock = self.stock.stock_df
        display_stock.index += 1
        print(display_stock)
        while True:
            print(print_banner(self.name, "Add Stock"))
            print(display_stock)
            print(item_dict)
            choice = input("\nPick an item to add: ").strip()
            if valid_option(choice, len(item_dict)) == False:
                print("Invalid option!")
                continue
            item_name = item_dict[choice][0].capitalize()
            amt = input(f"How many {item_name}")
            if valid_option(amt, self.stock.getCell(item_name, 'Stock'), True) == False:
                continue
            item_dict[choice][2] = int(amt)
            self.stock.addStock([item_dict[choice]])
        print(f"{amt} {item_name} added")
        enter_to_continue()
    
    def addItem(self):
        self.stock.updateStockDF()
        clear()
        print(print_banner(self.name, "Add Item to Stock"))
        item_to_add = [None]*4
        prompts = ["Item: ", "Category: ", "Price: ", "Stock: "]
        print(self.stock.stock_df.to_string(index = False))
        for i, prompt in enumerate(prompts):
            item_to_add[i] = input(prompt).strip()
            if i < 2:
                item_to_add[i] = item_to_add[i].lower().capitalize()
            else:
                item_to_add[i] = float(item_to_add[i])
        item_to_add = pd.DataFrame([item_to_add], columns = self.stock.stock_df.columns)
        self.stock.stock_df = self.stock.stock_df.append(item_to_add, ignore_index = True)
        self.stock.updateStockCSV()
        self.stock.updateActualStockCSV()

    def removeStock(self):
        self.stock.updateStockDF()
        clear()
        self.stock.showAll()
        print(print_banner(self.name, "Remove Stock"))
        stock_list = self.stock.stock_df.values
        item_dict = {}
        for i, item in enumerate(stock_list):
            item_dict[f"{i+1}"] = [item]
        display_stock = self.stock.stock_df
        display_stock.index += 1
        print(display_stock)
        choice = input("Pick an item to add: ")
        print(item_dict[choice])
        enter_to_continue()
        self.stock.addStock(item_dict[choice])

    def action(self):
        self.stock.updateStockDF()
        menu = MenuFunctions("View Stock", self.viewStock, "Restock",  self.restock, "Add Item", self.addItem, "Remove Stock", self.removeStock)
        menu.show_functions(self.name)
        self.stock.updateActualStockCSV()
        return False

class CheckUsers:
    def __init__(self, current_user):
        self.current_user = current_user
        self.name = "Check Users"
        self.login_stuff = LoginRegister()
        self.users = self.login_stuff.users
        self.users.index += 1
        self.stock = Stock()
    
    def updateDF(self):
        self.login_stuff.update_users()
        self.users = self.login_stuff.users

    def viewAllUsers(self):
        self.updateDF()
        print(self.users[['Username','account_type']])
        enter_to_continue()
    
    def addAdmin(self):
        self.updateDF()
        self.login_stuff.register(True)
    
    def removeUser(self):
        while True:
            clear()
            print(print_banner(self.name, "Remove User"))
            self.updateDF()
            user_remove = input("User to remove (0 to cancel): ").strip().lower()
            if self.current_user.lower() == user_remove:
                print("You can't remove yourself!")
                enter_to_continue()
            elif user_remove == "0":
                break
            elif user_remove in self.login_stuff.lower_user_list:
                self.users = self.users.drop(self.users.index[self.users['Username'] == user_remove], axis=0)
                self.users.to_csv('data/users.csv', index = False)
                print(f"{user_remove} removed.")
                enter_to_continue()
                break
            else:
                print("User does not exist!")
                enter_to_continue()
        
    def action(self):
        menu = MenuFunctions("View all users", self.viewAllUsers, "Add admin", self.addAdmin, "Remove user", self.removeUser)
        self.updateDF()
        menu.show_functions(self.name)
        self.updateDF()
        return False