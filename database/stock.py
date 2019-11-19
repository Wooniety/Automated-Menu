import pandas as pd
from database.utils import *
from database.common_menu import *


# Use the functions in Stock to mess directly with the csv. Shopping cart is seperate.

class Stock: 
    def __init__(self):
        self.name = "View stock"
        self.stock = pd.read_csv('data/menu.csv')
        self.categories = self.stock['Category'].unique()
        self.categories_data = {}
        for category in self.categories:
            self.categories_data[category] = self.stock[self.stock['Category'] == category] 

    def updateStockDF(self):
        self.stock = pd.read_csv('data/menu.csv')
        self.categories = self.stock['Category'].unique()
        for category in self.categories_data:
            self.categories_data[category] = self.stock[self.stock['Category'] == category] 

    def updateStockCSV(self):
        self.stock.to_csv('data/menu.csv', index = False)

    def removeStock(self):
        pass

    def addStock(self):
        pass

    def changeValue(self, value_column, value_row, new_value):
        self.updateStockDF()
        self.stock.at[value_row, value_column] = new_value
        print(self.stock)
        enter_to_continue()
        self.updateStockCSV()

    def showCategory(self, msg1 = "The following categories exist", msg2 = "Which category do you want to check?", return_df = True):
        self.updateStockDF()
        while True:
            clear()
            print(print_banner("Choose a category"))
            categories = {}
            print(msg1)
            for i, category in enumerate(self.categories):
                categories[f"{i+1}"] = category
                print(f"{i+1} {category}")
            category = input("\n" + msg2).strip()
            if category == "":
                print("Please don't leave a blank!")
                enter_to_continue()
            elif category == "0":
                return 0, 0
            elif categories[category] in self.categories_data:
                if return_df:
                    return self.categories_data[categories[category]], self.categories[int(category)-1]
                else:
                    print(self.categories_data[categories[category]])
            else:
                print("Category does not exist!\n")

    def showAll(self):
        self.updateStockDF()
        print(self.stock.to_string(index = False))
        enter_to_continue()
        
    def action(self):
        self.updateStockDF()
        self.functions = MenuFunctions("Show all stocked items", self.showAll, "Show category", self.showCategory)
        self.functions.show_functions(self.name)