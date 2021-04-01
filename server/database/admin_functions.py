# Import stuff
import pandas as pd
from database.utils import *
from database.common_menu import *
from database.stock import *

class ChangeStock:
    def __init__(self):
        self.name = "Stock"
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
    def __init__(self, current_user):
        self.current_user = current_user
        self.name = "Check Users"
        self.login_stuff = LoginRegister()
        self.users = self.login_stuff.users
        self.users.index += 1
 
    def updateDF(self):
        self.login_stuff.update_users()
        self.users = self.login_stuff.users

    def addAdmin(self):
        self.updateDF()
        self.login_stuff.register(True)
        self.updateDF()
    
    def removeUser(self, user_remove):
        self.updateDF()
        if self.current_user.lower() == user_remove:
            pass
        elif user_remove in self.login_stuff.lower_user_list:
            self.users = self.users.drop(self.users.index[self.users['Username'] == user_remove], axis=0)
            self.users.to_csv('data/users.csv', index = False)