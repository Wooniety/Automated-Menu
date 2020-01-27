import pandas as pd
from database.utils import *
from database.common_menu import *

# Use the functions in Stock to mess directly with the csv. Shopping cart is seperate.

class Stock: 
    def __init__(self):
        self.name = "View stock"
        # Client side stock
        self.stock_df = pd.read_csv('data/menu.csv')
        self.all_items = self.stock_df['Item'].unique()
        self.categories = self.stock_df['Category'].unique()
        self.categories_data = {}
        for category in self.categories:
            self.categories_data[category] = self.stock_df[self.stock_df['Category'] == category] 

    def readStockFromOG(self):
        """Update client side menu.csv from stock.csv"""
        # TODO If not in stock, do not display item
        self.og_stock = pd.read_csv('data/stock.csv')
        self.og_stock.to_csv('data/menu.csv', index = False)

    def updateStockDF(self): # Client stock dataframe
        """Update menu dataframe from menu.csv"""
        self.all_items = self.stock_df['Item'].unique()
        self.stock_df = pd.read_csv('data/menu.csv')
        self.categories = self.stock_df['Category'].unique()
        for category in self.categories_data:
            self.categories_data[category] = self.stock_df[self.stock_df['Category'] == category] 

    def updateStockCSV(self): # Updata temp stock. Updated to main stock when checking out.
        self.stock_df.to_csv('data/menu.csv', index = False)
    
    def updateActualStockCSV(self): 
        # Update actual database stock. Only use when checking out
        # That way if the user quits the program suddenly, stock reverts to normal
        self.stock_df.to_csv('data/stock.csv', index = False)

    # Utils to mess with the stock df
    def removeStock(self, item, num):
        self.updateStockDF()
        if item in self.all_items:
            if self.getCell(item, 'Stock') - num >=0:
                self.changeValue(item, 'Stock', self.getCell(item, 'Stock') - num)
            else:
                print("Too many!")
            if self.getCell(item, 'Stock') == 0:
                self.stock_df = self.stock_df.drop(self.stock_df.index[self.stock_df['Item'] == item], axis=0)
        else:
            print("Invalid input!")
        self.updateStockCSV()

    def addStock(self, item): # [[item, category, price, num]]
        self.updateStockDF()
        if item[0][0] in self.all_items:
            self.stock_df.loc[self.stock_df['Item'] == item[0][0], 'Stock'] += item[0][3]
        else:
            items_to_add = pd.DataFrame(item, columns = self.stock_df.columns)
            self.stock_df = self.stock_df.append(items_to_add, ignore_index = True)
        self.updateStockCSV()

    def getCell(self, value_row, value_column):
        self.updateStockDF()
        cell = self.stock_df.loc[self.stock_df['Item'] == value_row, value_column].values[0]
        return cell

    def changeValue(self, value_row, value_column, new_value):
        self.updateStockDF()
        self.stock_df.loc[self.stock_df['Item'] == value_row, value_column] = new_value
        self.updateStockCSV()
    
    # Admin functions and utils below
    def showCategory(self, msg1 = "The following categories exist", msg2 = "Which category do you want to check?", return_df = True):
        self.updateStockDF()
        while True:
            clear()
            print(print_banner("Choose a category"))
            categories = {}
            print(msg1)
            print("0) Go back")
            for i, category in enumerate(self.categories):
                categories[f"{i+1}"] = category
                print(f"{i+1}) {category}")
            category = input("\n" + msg2).strip()
            if category == "":
                print("Please don't leave a blank!")
                enter_to_continue()
            elif category == "0":
                return 0, 0, 0
            elif category in categories:
                if return_df:
                    return self.categories_data[categories[category]], self.categories[int(category)-1], category
                else:
                    print(self.categories_data[categories[category]])
            else:
                print("Category does not exist!\n")
                enter_to_continue()
    
    def searchStock(self, search): #Returns array of items that match the description
        results = []
        for item in self.all_items:
            if search.lower().strip() in item.lower():
                results.append(item)
        return results

    def showAll(self):
        self.updateStockDF()
        print(self.stock_df.to_string(index = False))
        enter_to_continue()
        
    def action(self): # Might not actually need this. Make a super class
        self.updateStockDF()
        self.functions = MenuFunctions("Show all stocked items", self.showAll, "Show category", self.showCategory, "Add Item", "Reduce Quantity", "Delete item")
        self.functions.show_functions(self.name)
        return 1
