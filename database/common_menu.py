# from database.user_functions import *
from database.macros import *
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
        while True:
            if self.menu_msg != None:
                print(self.menu_msg)
                self.menu_msg = None
            else:
                clear()
                print("Find something to do")
            for option in sorted(self.options):
                print(f"{option}: {self.options[option].name}")
            user_choice = input("\nPlease enter an option: ").strip()
            if user_choice == "":
                print("No option selected.\n")
            elif user_choice in self.options:
                return user_choice
            else:
                options_exists = False
                for option in sorted(self.options): # Check if user typed in option instead of number
                    if user_choice.lower() in self.options[option].name.lower():
                        if yes_or_no(f"{self.options[option].name}?"):
                            return option
                        else:
                            options_exists = True
                            continue
                if options_exists == False:
                    print(f"Sorry. I'm not sure what you mean by '{user_choice}'") 
                    sleep(1) #Show for a second before clearing screen

class Leave_Mall:
    def __init__(self):
        self.name = "Leave Mall"
    
    def action(self):
        clear()
        exit(0)

class Login_Register: #Not in use yet
    def __init__(self):
        self.name = "Login/Register"
        self.username = "User"
        self.password = "Password"
    
    def action(self):
        clear()
        exit(0)