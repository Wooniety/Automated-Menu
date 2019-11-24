import pandas as pd
import getpass
from database.utils import *

class Menu:
    def __init__(self, menu_msg = None, *options):
        self.menu_msg = menu_msg
        self.options = {} # "option number": class
        for i in range(0, len(options), 2):
            self.options[options[i]] = options[i+1] 

    def add_menu(self, *add_options):
        for i in range(0, len(add_options), 2):
            self.options[add_options[i]] = add_options[i+1]
    
    def remove_menu(self, key):
        del self.options[key]

    def show_menu(self):
        location = "Mall Entrance"
        while True:
            clear()
            if self.menu_msg != None:
                print(f"{print_banner(location)}As you approach the mall, a tired employee greets you.\n\nTired Employee: \"{self.menu_msg}\"\n")
                self.menu_msg = None
            else:
                print(print_banner(location))
                print("You stand at the entrance of the mall...\n")

            for option in sorted(self.options): # Print out available options
                print(f"{option}: {self.options[option].name}")
            user_choice = input("\nPlease enter an option: ").strip()

            if user_choice == "":
                print("No option selected.")
                enter_to_continue()
            elif user_choice in self.options: #If user types in option number
                return user_choice
            else:
                print(f"Sorry. I'm not sure what you mean by '{user_choice}'") 
                enter_to_continue()

class MenuFunctions:
    def __init__(self, *options): # Menu_Functions(option_name, function) 
        self.options = {"Go back": self.exit} # option_name: function;
        self.option_num = {"0": self.exit} # option_num: function
        for i in range(0, len(options), 2):
            self.options[options[i]] = options[i+1] 
            self.option_num[f"{int(i-i/2+1)}"] = options[i+1]

    def exit(self):
        pass

    def show_functions(self, function_msg = "", input_msg = "\nPlease enter an option: "):
        while True:
            clear()
            print(print_banner(function_msg))

            for i, option in enumerate(self.options):
                print(f"{i}) {option}")
            choice = input(f"{input_msg}").strip().lower()
            if choice == "go back" or choice == "0":
                return
            if choice in self.option_num:
                self.option_num[choice]()
            elif choice in self.options:
                self.options[choice]()
            else:
                print("Invalid option!")
                enter_to_continue()

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
        for user in self.user_list:
            self.lower_user_list.append(user.lower())
        self.user_list = self.users['Username'].unique()

    def login(self):
        while True:
            clear()
            print(print_banner(self.name, "Login"))
            find_user = input("Username: ")
            password = getpass.getpass("Password: ")
            if find_user.lower() in self.lower_user_list:
                user_password = self.users.loc[self.users['Username'] == find_user.lower(), 'password'].values[0]
                password = str(hashing(password))
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
        clear()
        print(print_banner(self.name, "Register"))
        user_details = [None]*3
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
        user_details[2] = acc_type
        clear()
        print(print_banner("Register"))
        print(f"Welcome {user_details[0]}!")
        enter_to_continue()

        # Tell main program name user details
        self.username = user_details[0]
        self.user_type = user_details[2]

        # Update database
        user_details[0] = user_details[0].lower()
        user_details[1] = hashing(user_details[1])
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