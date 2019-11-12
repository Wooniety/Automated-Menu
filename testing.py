import pandas as pd

class Stock:
    def __init__(self):
        self.name = "View stock"
        self.stock = pd.read_csv('data\menu.csv')
        self.categories = self.stock['Category'].unique()
        self.categories_data = {}
        for category in self.categories_data:
            self.categories_data[category] = self.stock[self.stock['Category'] == category]

    def action(self):
        self.show_category(self.categories[0])
    
    def show_category(self, category):
        category_data = self.categories_data[self.categories["Category"]]
        print(category_data)
        
    def update_csv(self):
        self.stock('data/menu.csv', index = False)

stocks = Stock()
stocks.action()