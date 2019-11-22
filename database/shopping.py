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

    def updateAisleData(self):
        self.stock.updateStockDF()
        categories = {}
        for i, category in enumerate(self.stock.categories):
            categories[f"{i+1}"] = category
        self.aisle_data = self.stock.categories_data[categories[self.category_num]]
        self.aisle_data = self.aisle_data[["Item", "Price", "Stock"]]

    def exploreAisle(self):
        clear()
        print(print_banner(self.name))

        # Seperate the items into different dataframes for categories
        self.aisle_data, self.aisle_name, self.category_num = self.stock.showCategory("You see a sign point to different aisles", "Which aisle do you go down?\n")
        if self.aisle_name == 0:
            self.exit = False
        else:
            self.aisle_data = self.aisle_data[["Item", "Price", "Stock"]]

    def getItemFromAisle(self):
        category_items = {"0": None}
        choice = None

        while choice != "0":         
            self.cart.refreshCartDF()
            self.updateAisleData()
            for i, item in enumerate(self.aisle_data.values):
                category_items[f"{i+1}"] = [item[0], item[1], int(item[2])] #[Item, price, stock]
            clear()

            print(print_banner(self.name, self.aisle_name))
            print("The items on the shelves stare back at you...")
            print("0) Don't add item to cart\n")
            print("   Items      Price   In stock")
            for i, item in enumerate(self.aisle_data.values):
                print(f"{i+1}) {item[0]}{get_spaces(10-len(item[0]))} {item[1]}{get_spaces(7-len(str(item[1])))} {int(item[2])}")# While not exit
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
                    print(f"Selected item: \033[1;33;40m{category_items[choice][0]} ({category_items[choice][2]})\033[0;37;40m\n")
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
                    category_items[choice][2] -= amt
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
        return False

class ShoppingCart:
    def __init__(self):
        self.name = "View items" # TODO: items/basket/cart
        self.cart = pd.read_csv("data/cart.csv")
        self.stock = Stock()

    def action(self):
        while True:
            self.refreshCartDF()
            clear()
            print(print_banner("View Cart"))
            cart, empty = self.viewCart(True)
            print(cart)
            if empty:
                enter_to_continue()
            if self.cart_empty:
                break
            else:
                if yes_or_no("Do you want to remove anything from the cart?"):
                    items_to_remove = {}
                    for i, item in enumerate(self.items_in_cart):
                        items_to_remove[f"{i+1}"] = item
                    choice = input("Which item do you want to remove? (0 to cancel)\n").strip()
                    if choice == "0":
                        pass
                    elif choice in items_to_remove:
                        while True:
                            amt = input("How many?\n").strip()
                            if if_num(amt):
                                amt = int(amt)
                                if amt > len(self.items_in_cart) or amt < 0:
                                    print("Invalid number!")
                                else:
                                    break
                            else:
                                print("Invalid input!")
                        self.removeFromCart(items_to_remove[choice], amt)
                else:
                    enter_to_continue()
                    break
        return False
                

    def refreshCartDF(self):
        self.cart = pd.read_csv("data/cart.csv")
        self.items_in_cart = self.cart['Items'].unique()
    
    def updateToCart(self):
        self.cart.to_csv('data/cart.csv', index = False)

    def addItemToCart(self, items):
        '''
        items is a list [[item, quantity, price]]
        For the dataframe it needs the array to be like this [[]]
        '''
        self.refreshCartDF()
        if items[0][0] in self.items_in_cart:
            self.cart.loc[self.cart['Items'] == items[0][0], 'Quantity'] += items[0][1]
            self.cart.loc[self.cart['Items'] == items[0][0], 'Price'] += items[0][2]*items[0][1]
        else:
            items_to_add = pd.DataFrame(items, columns = self.cart.columns)
            self.cart = self.cart.append(items_to_add, ignore_index = True)
        self.stock.changeValue(items[0][0], 'Stock', self.stock.getCell(items[0][0], 'Stock') - items[0][1])
        # if self.stock.getCell(items[0][0], 'Stock') <= 0:
        #     self.stock
        self.updateToCart()
    
    def removeFromCart(self, item, num_of_items): # removeFromCart("Milk", 1, 3)
        self.refreshCartDF()
        item = item.lower().capitalize()
        if item in self.items_in_cart:
            self.cart.loc[self.cart['Items'] == item, 'Quantity'] -= num_of_items
            self.cart.loc[self.cart['Items'] == item, 'Price'] -= num_of_items*self.stock.getCell(item, "Price")
            if self.cart.loc[self.cart['Items'] == item, 'Quantity'].values[0] <= 0:
                self.cart = self.cart.drop(self.cart.index[self.cart['Items'] == item], axis=0)
                
            self.updateToCart()
        else:
            print("Item does not exist in cart!")
    
    def viewCart(self, show_index = False):
        self.cart = pd.read_csv("data/cart.csv")
        self.cart.index += 1
        if self.cart.empty:
            self.cart_empty = True
            return "There is nothing in the cart!", True
        else:
            self.cart_empty = False
            return self.cart.to_string(index=show_index), False

class Checkout:
    def __init__(self):
        self.name = "Checkout"
        self.cart = ShoppingCart()
        self.stock = Stock()
    
    def getTotalAmt(self): # self.total is the total price of all items
        total = self.cart.cart[['Price']].copy()
        total = total.sum().sum()
        return float(total)

    def action(self):
        print_cart, empty = self.cart.viewCart()
        print(print_cart)
        print(f"Your total amount is: ${to_num(self.getTotalAmt(), True, 2)}")
        choice = yes_or_no("Do you want to check out?")
        if choice:
            clear_cart()
            clear()
            print_banner("Checkout")
            print("Thanks for shopping with the Krusty Krabz!")
            self.stock.updateActualStockCSV()