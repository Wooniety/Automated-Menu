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

    def show_category(self):
        while True:
            categories = {}
            print("The following categories exists")
            for i, category in enumerate(self.categories):
                categories[f"{i+1}"] = category
                print(f"{i+1} {category}")
            category = input("Which category do you want to check?").strip()
            if categories[category] in self.categories_data:
                print(self.categories_data[category].to_string(index = False))
                return
            else:
                print("Category does not exist!\nAvailable categories:\n")

    def show_all(self):
        print(self.stock.to_string(index = False))
        
    def action(self):
        self.functions = MenuFunctions("Show all stocked items", self.show_all, "Show category", self.show_category)
        self.functions.show_functions()