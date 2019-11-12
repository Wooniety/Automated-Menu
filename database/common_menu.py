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

            for option in sorted(self.options): # Print out available options
                print(f"{option}: {self.options[option].name}")
            user_choice = input("\nPlease enter an option: ").strip()

            if user_choice == "":
                print("No option selected.\n")
            elif user_choice in self.options: #If user types in option number
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
                if options_exists == False: # Can't do else because 'continue' would still trigger else
                    print(f"Sorry. I'm not sure what you mean by '{user_choice}'") 
                    sleep(1) #Show for a second before clearing screen

class Menu_Functions:
    def __init__(self, *options): # Menu_Functions(option_name, function) 
        self.options = {} # option_name: function
        self.option_num = {} # option_num: function
        for i in range(0, len(options), 2):
            self.options[options[i]] = options[i+1] 
            self.option_num[f"{i}"] = options[i+1]
    
    def show_functions(self, msg = None):
        for i, option in enumerate(self.options):
            print(f"{i}) {option}")
        if msg == None:
            msg == "Please pick an option\n"
        print("\n")
        while True:
            choice = input(f"{msg}")
            if choice == "":
                print("No option selected")
            elif choice.isnumeric():
                if choice in self.option_num:
                    self.option_num[choice]
                    return
                else:
                    print("Invalid option!")
            else:
                if choice in self.options:
                    self.options[choice]
                    return
                else:
                    print("Invalid option!")
