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

    def login(self):
        """Existing user"""
        while True:
            clear()
            print(print_banner(self.name, "Login"))
            find_user = input("Username: ")
            password = getpass.getpass("Password: ") # Hides input
            self.update_users()
            if find_user.lower() in self.lower_user_list:
                user_password = self.users.loc[self.users['Username'] == find_user.lower(), 'password'].values[0]
                user_salt = self.users.loc[self.users['Username'] == find_user.lower(), 'salt'].values[0]
                password = hashing(password, user_salt)
                if password == user_password:
                    self.username = find_user
                    self.user_type = self.users.loc[self.users['Username'] == self.username.lower(), 'account_type'].values[0]
                    print(f"Welcome back {self.username}!")
                    enter_to_continue()
                    return 0
            choice = yes_or_no("Invalid credentials! Go back?")
            if choice:
                return 1

    def register(self, admin = False):
        """Create new account"""
        clear()
        print(print_banner(self.name, "Register"))
        user_details = [None]*4 # username, password, salt, acc_type
        if admin:
            header = "Admin Console"
            msg = "Enter admin details"
            acc_type = "Admin"
        else:
            header = self.name
            msg = "Welcome! I see this is your first time here! Before we get into the program, please tell me a bit about yourself!\n"
            acc_type = "Customer"
        while True:
            clear()
            print(print_banner(header, "Register"))
            print(msg)
            user_details[0] = input("Username: ").strip()
            self.update_users()
            if user_details[0] == "":
                print("Enter a Username!")
                continue
            elif user_details[0].lower() in self.lower_user_list:
                choice = yes_or_no("Username taken. Cancel?")
                if choice:
                    return 1
                else:
                    continue
            user_details[1] = getpass.getpass("Password: ")
            user_details[2] = getpass.getpass("Enter password again: ")
            if user_details[1] != user_details[2]:
                print("Passwords do not match!")
                enter_to_continue()
            elif user_details[1].strip() == "":
                print("Enter a password!")
            else:
                break
        user_details[3] = acc_type
        clear()
        print(print_banner("Register"))
        print(f"Welcome {user_details[0]}!")
        enter_to_continue()

        # Tell main program name user details
        self.username = user_details[0]
        self.user_type = user_details[3]

        # Update database
        user_details[0] = user_details[0].lower()
        user_details[2] = bcrypt.gensalt().decode()
        user_details[1] = hashing(user_details[1], user_details[2]) # Hashes the password
        user_details = pd.DataFrame([user_details], columns = self.users.columns)
        self.users = self.users.append(user_details, ignore_index = True)
        self.users.to_csv('data/users.csv', index=False)
        return 0

    def action(self):
        while True:
            self.update_users()
            clear()
            print(print_banner(self.name))
            choice = yes_or_no("Is this your first time here?")

            # Login or register
            if choice:
                choice = self.register()
            else:
                choice = self.login()

            # If user cancels, return 1
            if choice == 0: 
                break