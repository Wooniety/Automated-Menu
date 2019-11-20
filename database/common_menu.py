# from database.user_functions import *
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