import pandas as pd
import getpass
from database.utils import *

class Menu:
    """Feed this classes.\n
    Each class has a self.name which is the name of the option to be displayed,
    as well as self.action() which will run as a function that leads to other functions."""
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
    """A menu class for functions instead of classes"""
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
    
    def user_login(self):
        """Existing user"""
        clear()
        print(print_banner(self.name, "Login"))
        self.username = input("Username: ")
        self.password = getpass.getpass("Password: ") # Hides input

    def register(self, admin = False):
        """Create new account"""
        clear()
        print(print_banner(self.name, "Register"))
        user_details = [None]*3 # username, password, check password
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
            # elif user_details[0].lower() in self.lower_user_list:
            #     choice = yes_or_no("Username taken. Cancel?")
            #     if choice:
            #         return 1
            #     else:
            #         continue
            user_details[1] = getpass.getpass("Password: ")
            user_details[2] = getpass.getpass("Enter password again: ")
            if user_details[1] != user_details[2]:
                print("Passwords do not match!")
                enter_to_continue()
            elif user_details[1].strip() == "":
                print("Enter a password!")
            else:
                break
        clear()
        print(print_banner("Register"))
        print(f"Welcome {user_details[0]}!")
        enter_to_continue()

        # Tell main program name user details
        self.username = user_details[0]
        self.password = user_details[1]
        self.user_type = acc_type

    def action(self):
        clear()
        print(print_banner(self.name))
        choice = yes_or_no("Is this your first time here?")

        # Login or register
        if choice:
            self.register()
            return 0
        else:
            self.user_login()
            return 1
        # If user cancels, return 1
        #if choice == 0: 
        #    break
    
    def getUsers(self):
        self.users = pd.read_csv("data/users.csv")
        self.user_list = self.users['Username'].unique()
        self.lower_user_list = []
        for user in self.user_list:
            self.lower_user_list.append(user.lower())