import pandas as pd
from database.utils import *
from database.common_menu import *
from database.stock import *

class GetCarrier:
    def __init__(self):
        self.name = "Get shopping cart/basket"
    def action(self):
        pass

class ExploreAisle:
    def __init__(self):
        self.name = "Explore the shopping aisle"
        self.stock = Stock()
        self.cart = ShoppingCart()
    
    def searchForItem(self):
        pass #TODO

    def exploreAisle(self):
        clear()
        print(print_banner(self.name))

        # Seperate the items into different dataframes for categories
        self.aisle_data, self.aisle_name = self.stock.showCategory("You see a sign point to different aisles", "Which aisle do you go down?\n")
        if self.aisle_name == 0:
            self.exit = False
        else:
            self.aisle_data = self.aisle_data[["Item", "Price", "Stock"]]

    def getItemFromAisle(self):
        category_items = {"0": None}
        # put items in aisle into a dictionary to select. 
        for i, item in enumerate(self.aisle_data.values):
            category_items[f"{i+1}"] = [item[0], item[1], item[2]] #[Item, price, stock]

        print(category_items)
        # print(max(category_items.values))

        choice = None

        while choice != "0":         
            clear()
            print(print_banner(self.name, self.aisle_name))
            print("The items on the shelves stare back at you...")
            print("0) Don't add item to cart")
            for i, item in enumerate(self.aisle_data.values):
                print(f"{i+1}) {item[0]} {item[1]} {item[2]}")# While not exit
            choice = input("\nAdd an item to cart?\n")
            clear()
            print(print_banner(self.name, self.aisle_name))
            if choice == "":
                print("Please enter something!")
            elif choice == "0":
                break
            elif choice in category_items: # Item chosen to add to cart
                while True: # Check if valid number added to cart
                    clear()
                    print(print_banner(self.name, self.aisle_name))
                    print(f"Selected item: \033[1;33;40m{category_items[choice][0]}\033[0;37;40m\n")
                    amt = input("Number to add (0 to stop): ").strip()

                    if amt == "" :
                        print("Please enter an amount!")
                        enter_to_continue()
                        continue
                    elif if_num(amt):
                        amt = int(amt)
                    else:
                        amt = -1
                    if amt > category_items[choice][2]:
                        print("That's too many!")
                        enter_to_continue()
                        continue
                    elif amt >= 0:
                        break
                    print("Invalid option!")
                    enter_to_continue()
                if amt == 0: # Don't add anything
                    pass
                else:
                    to_cart = [[category_items[choice][0], amt, category_items[choice][1]]]
                    self.cart.addItemToCart(to_cart)
                    print(f"Added {amt} {category_items[choice][0]} to cart")
                    enter_to_continue()
            else:
                print("Invalid option!")
                enter_to_continue()

    def action(self):
        self.exit = True
        self.exploreAisle()
        while self.exit:
            self.getItemFromAisle()
            self.exploreAisle()
            enter_to_continue()

class ShoppingCart:
    def __init__(self):
        self.name = "View items" # TODO: items/basket/cart
        self.cart = pd.read_csv("data/cart.csv")

    def action(self):
        self.functions = MenuFunctions("View cart", self.viewCart)
        self.functions.show_functions(self.name)
    
    def updateToCart(self):
        self.cart.to_csv('data/cart.csv', index = False)

    def addItemToCart(self, items):
        '''
        items is a list [[item, quantity, price]]
        For the dataframe it needs the array to be like this [[]]
        '''
        items_in_cart = self.cart['Items'].unique()
        if items[0][0] in items_in_cart:
            self.cart.at[items[0][0], 'Quantity'] = 10
        else:
            items_to_add = pd.DataFrame(items, columns = self.cart.columns)
            self.cart = self.cart.append(items_to_add, ignore_index = True)
        self.updateToCart()
    
    def removeFromCart(self, item, num_of_items):
        if item in self.cart.index:
            num_in_cart = self.cart.at[item, "Quantity"]
            num_in_cart -= num_of_items
            if num_in_cart < 1:
                data = data.drop([item], axis=1)
        else:
            print("Item does not exist!")
    
    def viewCart(self):
        self.cart = pd.read_csv("data/cart.csv")
        if self.cart.empty:
            print("There is nothing in the cart!")
            enter_to_continue()
        else:
            print(self.cart.to_string(index=False))
            enter_to_continue()