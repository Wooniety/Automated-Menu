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
    
    def action(self):
        stock = Stock()
        section = "Explore the aisles"
        print(print_banner(section))
        aisle_data, aisle_name = stock.show_category("You see a sign point to different aisles", "Which aisle do you go down?\n")
        clear()
        print(print_banner(section, aisle_name))
        print(aisle_data)
        enter_to_continue()
        """
        cart = ShoppingCart()
        cart = cart.add_to_cart("Cheese", 2) 
        cart.view_cart()
        sleep(10)
        """

class ShoppingCart:
    def __init__(self):
        self.name = "View items" # TODO: items/basket/cart
        self.cart = pd.DataFrame(columns=["Items", "Quantity"])

    def action(self):
        self.functions = MenuFunctions("View cart", self.view_cart)
        self.functions.show_functions(self.name)

    def add_to_cart(self, item, num_of_items):
        if item in self.cart.index:
            num_in_cart = self.cart.at[item, "Quantity"]
            num_in_cart += num_of_items
            return num_in_cart
        else:
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
            enter_to_continue()
        else:
            print(self.cart)
            enter_to_continue()