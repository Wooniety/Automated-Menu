# SPAM Menu

You have a cart and you can run free in the confines of the CLI which hosts the Krusty Krabz

## Prerequisites

- Python 3.7 (Not 3.8)
- Pandas
  - https://pandas.pydata.org/pandas-docs/stable/install.html
- Bcrypt
  - https://pypi.org/project/bcrypt/

## How to run

If cloning from Github

``` bash
git clone https://github.com/Wooniety/SPAM-Menu
cd SPAM-Menu
python main.py
```

If already cloned:

``` bash
python {directory_to_folder}/SPAM-Menu/main.py
```

## Features

### Login/Register

You need to create an account!

Admin accounts exist but since the passwords are hashed you won't be logging in.
> Or just login as admin using the password 'admin' without quotation marks since this is just a joke program.

### The User Experience

Explore the different isles with their varying items!
> Ok not that much but sufficient

- Frozen Goods
- Drinks
- Bread
- Sweets
- Snacks

Or simply just search for it...

#### Discounts

Discount Sunday is thing. Or should it be called Sunday Sales?

### Admin Features

#### User system

- View Users
- Add more admins
- Remove users

#### Stock system

- Restock items
- Add more items
- Remove items

## Misc

### Woah Security

We hash your password with bcrypt.  
More to be added.

### Why Pandas?

- I wanted to learn it
- Already puts the data into a nice table
- Useful functions like `sum` and 'unique()' to sort the categories
- Reading from CSV and manipulating the data is really useful
