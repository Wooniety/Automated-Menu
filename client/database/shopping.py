# Import stuff
import pandas as pd
from database.utils import *
from database.common_menu import *
from database.stock import *

class ExploreAisle:
    """Get item by category"""
    def __init__(self):
        self.name = "Explore the shopping aisle"
        self.stock = Stock()
        self.cart = ShoppingCart()

    # Update the aisle dataframe whenever stuff like stock changes.
    def updateAisleData(self):
        """Refresh Items"""
        self.stock.updateStockDF()
        categories = {}
        for i, category in enumerate(self.stock.categories):
            categories[f"{i+1}"] = category
        self.aisle_data = self.stock.categories_data[categories[self.category_num]]
        self.aisle_data = self.aisle_data[["Item", "Price", "Stock"]]

    def exploreAisle(self):
        """Display different categories and get category data"""
        clear()
        print(print_banner(self.name))

        # Seperate the items into different dataframes for categories
        self.aisle_data, self.aisle_name, self.category_num = self.stock.showCategory("You see a sign point to different aisles", "Which aisle do you go down?\n", True)
        if self.aisle_name == 0:
            self.exit = False
        else:
            self.aisle_data = self.aisle_data[["Item", "Price", "Stock"]]

    def getItemFromAisle(self):
        """Add item from category to cart"""
        category_items = {"0": None}
        choice = None

        # While not exit
        while choice != "0":         
            self.cart.refreshCartDF()
            self.updateAisleData()
            
            # Add items from a category into a dictionary to refer to.
            for i, item in enumerate(self.aisle_data.values):
                category_items[f"{i+1}"] = [item[0], item[1], int(item[2])] #[Item, price, stock]
            clear()

            """
            0) Don't add item to cart

               Items    Price   In stock
            1) Chicken  $5.20   14
            """
            print(print_banner(self.name, self.aisle_name))
            print("The items on the shelves stare back at you...")
            print("0) Don't add item to cart\n")
            print("   Items        Price   In stock")
            for i, item in enumerate(self.aisle_data.values):
                # option_num) Item, price, stock
                print(f"{i+1}) {item[0]}{get_spaces(12-len(item[0]))} ${item[1]}{get_spaces(7-len(str(item[1])))} {int(item[2])}") 

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
                    elif amt.isnumeric():
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
                    category_items[choice][2] -= amt
                    self.cart.addItemToCart(category_items[choice][0], amt, category_items[choice][1]*amt, get_time())
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

class SearchItem:
    def __init__(self):
        self.name = "Search for item"
        self.cart = ShoppingCart()
        self.stock = Stock()

    def action(self):
        clear()
        print(print_banner("The shopping aisles", "Search for item"))
        find_item = input("Enter search query: ")
        found_items = self.stock.searchStock(find_item)
        if len(found_items) > 0:
            print("You found the following things that match your search: ")
            all_items = {}
            print(f"   Item:        Price:  In stock:")
            for i, item in enumerate(found_items):
                all_items[f"{i+1}"] = item
                print(f"{i+1}) {item}{get_spaces(12-len(item))} {self.stock.getCell(item, 'Price')}{get_spaces(7-len(str(self.stock.getCell(item, 'Price'))))} {self.stock.getCell(item, 'Stock')}") # Option num) item (stock)
            choice = yes_or_no("Do you want to add it to your cart?")
            if choice:
                while True:
                    choose_item = input("Item number: ").strip()
                    if valid_option(choose_item, len(all_items)):
                        choose_item = all_items[choose_item]
                        break
                    else:
                        print("Invalid option!")
                while True:
                    amt = input(f"Number of {choose_item}: ").strip()
                    if valid_option(amt, self.stock.getCell(choose_item, 'Stock'), True):
                        amt = int(amt)
                        break
                print(f"Added {amt} {choose_item} to cart")
                self.cart.addItemToCart(choose_item, amt, round_off(self.stock.getCell(choose_item, 'Price')*amt, 2), get_time())
        else:
            print("You couldn't find anything...")
        enter_to_continue()
        return False

class ShoppingCart:
    def __init__(self):
        self.name = "View items"
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
                            clear()
                            print(print_banner("View Cart"))
                            print(self.cart)
                            print(f"Which item do you want to remove? (0 to cancel)\n{items_to_remove[choice]}")
                            amt = input(f"How many {items_to_remove[choice]}?\n").strip()
                            if valid_option(amt, int(self.cart.loc[int(choice), 'Quantity']), True):
                                amt = int(amt)
                                break
                            else:
                                print("Invalid input!")
                                enter_to_continue()
                        print(f"{amt} {items_to_remove[choice]} removed.")
                        enter_to_continue()
                        self.removeFromCart(items_to_remove[choice], amt, get_time())
                else:
                    enter_to_continue()
                    break
        return False
                

    def refreshCartDF(self):
        self.cart = pd.read_csv("data/cart.csv")
        self.items_in_cart = self.cart['Items'].unique()
    
    def updateToCart(self):
        self.cart.to_csv('data/cart.csv', index = False)

    def addItemToCart(self, item, quantity, total_price, time):
        items = [[item, quantity, total_price, time]]
        self.refreshCartDF()
        if quantity == 0:
            # Don't add anything
            pass
        elif item in self.items_in_cart:
            # No. item in cart += amt to add
            self.cart.loc[self.cart['Items'] == item, 'Quantity'] += quantity
            # Price of item in cart += price of 1 x quantity
            self.cart.loc[self.cart['Items'] == item, 'Price'] += total_price 
            # Update time
            self.cart.loc[self.cart['Items'] == item, 'Last Modified'] = time
        else:
            items_to_add = pd.DataFrame(items, columns = self.cart.columns)
            self.cart = self.cart.append(items_to_add, ignore_index = True)
        self.stock.changeValue(item, 'Stock', self.stock.getCell(item, 'Stock') - quantity)
        # if self.stock.getCell(item, 'Stock') <= 0:
        #     self.stock
        self.updateToCart()
    
    def removeFromCart(self, item, num_of_items, time):
        self.refreshCartDF()
        self.stock.updateStockDF()
        if item in self.items_in_cart:
            # Add back to stock
            self.stock.changeValue(item, 'Stock', self.stock.getCell(item, 'Stock')+num_of_items)
            # Remove from cart
            self.cart.loc[self.cart['Items'] == item, 'Quantity'] -= num_of_items
            self.cart.loc[self.cart['Items'] == item, 'Price'] -= num_of_items*(self.stock.getCell(item, 'Price'))
            self.cart.loc[self.cart['Items'] == item, 'Last Modified'] = time
            # Remove item completely from cart if 0 or less
            if self.cart.loc[self.cart['Items'] == item, 'Quantity'].values[0] <= 0:
                self.cart = self.cart.drop(self.cart.index[self.cart['Items'] == item], axis=0)
            self.updateToCart()
        else:
            print("Item does not exist in cart!")
            enter_to_continue()
    
    def viewCart(self, show_index = False):
        self.cart = pd.read_csv("data/cart.csv")
        self.cart.index += 1
        if self.cart.empty:
            self.cart_empty = True
            return "There is nothing in the cart!", True
        else:
            self.cart_empty = False
            return self.cart.to_string(index=show_index), False
    
    def getCell(self, value_row, value_column):
        self.refreshCartDF()
        cell = self.cart.loc[self.cart['Items'] == value_row, value_column].values[0]
        return cell

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
        total_amt = to_num(self.getTotalAmt(), True, 2)

        # Apply discount on discount day
        discount_day = "Tuesday"
        if get_day() == discount_day:
            total_amt = to_num(total_amt*0.05, True, 2)
            print(f"Since today is {discount_day}, 5% off all items!")
        print(f"Your total amount is: ${total_amt}")
        choice = yes_or_no("Do you want to check out?")
        if choice:
            clear()
            print_banner("Checkout")
            print("Thanks for shopping with the Krusty Krabz!")
            self.stock.updateActualStockCSV()
            enter_to_continue()
        else:
            return False