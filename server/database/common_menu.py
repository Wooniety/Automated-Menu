import pandas as pd
import getpass
import traceback

from database.utils import *

class LoginRegister:
    def __init__(self):
        self.name = "Login/Register"
        self.users = pd.read_csv("data/users.csv")
        self.user_list = self.users['Username'].unique()
        self.lower_user_list = []
        for user in self.user_list:
            self.lower_user_list.append(user.lower())
    
    def update_users(self):
        self.users = pd.read_csv("data/users.csv")
        self.user_list = self.users['Username'].unique()
        for user in self.user_list:
            self.lower_user_list.append(user.lower())

    def check_login(self, find_user, password):
        self.update_users()
        if find_user.lower() in self.lower_user_list:
            user_password = self.users.loc[self.users['Username'] == find_user.lower(), 'password'].values[0]
            user_salt = self.users.loc[self.users['Username'] == find_user.lower(), 'salt'].values[0]
            password = hashing(password, user_salt)
            if password == user_password:
                self.username = find_user
                self.user_type = self.users.loc[self.users['Username'] == self.username.lower(), 'account_type'].values[0]
                return self.user_type
        print(f"{get_time()} - 200 Invalid login attempt at {find_user}")
        return '-1'

    def register(self, username, password, acc_type):
        """Create new account"""
        username = username.lower()
        salt = bcrypt.gensalt().decode()
        password = hashing(password, salt) # Hashes the password
        user_details = pd.DataFrame([[username, password, salt, acc_type]], columns = self.users.columns)
        self.users = self.users.append(user_details, ignore_index = True)
        self.users.to_csv('data/users.csv', index=False)