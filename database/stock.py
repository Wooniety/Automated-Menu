import pandas as pd
from database.macros import *

# Use the functions in Stock to mess directly with the csv. If just reading e.g shopping cart, DO NOT USE 

class Stock: 
    def __init__(self):
        self.name = "View stock"
        self.stock = pd.read_csv('data\menu.csv')
        self.categories = self.stock['Category'].unique()
        self.categories_data = {}
        for category in self.categories_data:
            each_cat = self.stock[self.stock['Category' == category]] 
            self.categories_data[category] = {each_cat}

    def update_stock_df(self):
        self.stock = pd.read_csv('data\menu.csv')
        self.categories = self.stock['Category'].unique()
        for category in self.categories_data:
            each_cat = self.stock[self.stock['Category' == category]] 
            self.categories_data[category] = {each_cat}

    def update_csv(self):
        self.stock('data\menu.csv', index = False)

    def show_category(self, category):
        if category in self.categories_data:
            print (self.categories_data[category])
        else:
            print("Category does not exist!")
        sleep(10)
    
    def show_categories(self):
        print("The following categories exist")
        
    def action(self):
        self.show_category("Frozen goods")