# SPAM Menu

You have a cart and you can run free in the confines of the CLI which hosts the Krusty Krabz

Also now we have a client-server thing going on.

## Prerequisites

- Python 3.7 (Not 3.8)
- [Pandas](https://pandas.pydata.org/pandas-docs/stable/install.html)
```bash
pip install pandas
```
- [Bcrypt](https://pypi.org/project/bcrypt/)
```bash
pip install bcrypt
```

## How to run

1) Clone from Github

``` bash
git clone https://github.com/Wooniety/SPAM-Menu
```

2) Start the server (Localhost)

```bash
python {directory_to_folder}/SPAM-Menu/server/main.py
```

3) Start the main program

``` bash
python {directory_to_folder}/SPAM-Menu/client/main.py
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

### Some security

#### Your passwords are somewhat safe

Hashed and salted with bcrypt.
> If you want to try using the sample accounts here, the passwords are the username.

## Misc

### Why Pandas?

- I wanted to learn it
- Already puts the data into a nice table
- Useful functions like `sum` and 'unique()' to sort the categories
- Reading from CSV and manipulating the data is really useful
