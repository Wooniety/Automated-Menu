import pandas as pd
from database.utils import *

class Shopping:
    def __init__(self):
        self.name = "Explore the shopping aisle"
    
    def action(self):
        cart = Shopping_Cart()
        cart = cart.add_to_cart("Cheese", 2) 
        cart.view_cart()
        sleep(10)

class Shopping_Cart:
    def __init__(self):
        self.cart = pd.DataFrame(columns=["Items", "Quantity"])

    def add_to_cart(self, item, num_of_items):
        if item in self.cart.index:
            num_in_cart = self.cart.at[item, "Quantity"]
            num_in_cart += num_of_items
            return num_in_cart
        else:
            items = [["food", 1]] ##Hard coded
            items_to_add = pd.DataFrame(items, columns = self.cart.columns)
            return self.cart.append(items_to_add, ignore_index = True)
    
    def remove_from_cart(self, item, num_of_items):
        if item in self.cart.index:
            num_in_cart = self.cart.at[item, "Quantity"]
            num_in_cart -= num_of_items
            if num_in_cart < 1:
                data = data.drop([item], axis=1)
        else:
            print("Item does not exist!")

    
    def view_cart(self):
        if self.cart.empty:
            print("There is nothing in the cart!")
        else:
            print(self.cart)