import pandas as pd
from database.utils import *
from database.common_menu import *


# Use the functions in Stock to mess directly with the csv. If just reading e.g shopping cart, DO NOT USE 

class Stock: 
    def __init__(self):
        self.name = "View stock"
        self.stock = pd.read_csv('data/menu.csv')
        self.categories = self.stock['Category'].unique()
        self.categories_data = {}
        for category in self.categories:
            self.categories_data[category] = self.stock[self.stock['Category'] == category] 

    def update_stock_df(self):
        self.stock = pd.read_csv('data/menu.csv')
        self.categories = self.stock['Category'].unique()
        for category in self.categories_data:
            self.categories_data[category] = self.stock[self.stock['Category'] == category] 

    def update_csv(self):
        self.stock('data/menu.csv', index = False)

    def show_category(self, msg1 = "The following categories exist", msg2 = "Which category do you want to check?"):
        clear()
        print(print_banner("Choose a category"))
        while True:
            categories = {}
            print(msg1)
            for i, category in enumerate(self.categories):
                categories[f"{i+1}"] = category
                print(f"{i+1} {category}")
            category = input("\n" + msg2).strip()
            if category == "":
                print("Please don't leave a blank!")
            elif categories[category] in self.categories_data:
                return self.categories_data[categories[category]], self.categories[int(category)-1]
            else:
                print("Category does not exist!\n")

    def show_all(self):
        print(self.stock.to_string(index = False))
        
    def action(self):
        self.functions = MenuFunctions("Show all stocked items", self.show_all, "Show category", self.show_category)
        self.functions.show_functions(self.name)