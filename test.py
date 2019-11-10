import pandas as pd

menu = pd.read_csv('data\menu.csv')
test = pd.read_csv('data\Test.csv')

categories = menu['Category'].unique()

sorted_stuff = {}

# Print by category
for cat in categories:
    each_cat = menu[menu['Category'] == cat]
    sorted_stuff[cat] = each_cat


frozen = sorted_stuff[categories[0]]
frozen_items = frozen[['Item', 'Price']]
for i, item in enumerate(frozen.values):
    print(f"{i+1}) {item[1]} {item[2]}")

def addItemIntoMenu(items, df):
    '''
    items is a list [[category, item, price, stock], ...[]]
    For the dataframe it needs the array to be like this [[]]
    '''
    items_to_add = pd.DataFrame(items, columns = df.columns)
    df = df.append(items_to_add, ignore_index = True)
    return df

menu = addItemIntoMenu([['Drinks', 'Sprite', 10, 10]], menu)
print(menu)

# Reading out dataframes with paths
menu.to_csv('data/menu.csv', index = False)

# for item, row in frozen_items.iterrows():
#     print(f"{item}) {row['Item']}   ${row['Price']}")
# for item in frozen_items:
#    print(item)
# print(frozen['Item', 'Price'])
# print(frozen['Item', 'Price'])

# frozen_items = frozen.loc[frozen['Item'] == 1]
# print(menu.groupby(['Category']))

# print(pd.DataFrame.equals(menu, test))
# print(menu.head(2))

# add_items = {
#     'Category': 'Drinks',
#     'Item': 'Tea',
#     'Price': 3.5
# }

# add_items = [[10, 'Drinks', 'Tea', 3.5, 30],[9, 'a', 'A', 6.9, 2]]

# print(data.columns)

# add_items = pd.DataFrame(add_items, columns= data.columns)

# print(add_items)

# data = data.append(add_items)

# data.loc[-1] = add_items
# data.index = data.index + 1

# print(menu)

# print(categories)

# print(data.head())