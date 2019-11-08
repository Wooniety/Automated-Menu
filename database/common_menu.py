from database.macros import *

class Menu:
    def __init__(self, *options):
        self.options = {}
        for i in range(0, len(options), 2):
            self.options[options[i]] = options[i+1] 

    def add_menu(self, *options):
        for i in range(0, len(options), 2):
            self.options[options[i]] = options[i+1]
    
    def remove_menu(self, key):
        del self.options[key]

    def show_menu(self):
        while True:
            print("Find something to do")
            for option in sorted(self.options):
                print(f"{option}) {(self.options[option]).name}")
            user_choice = input("Please enter an option: ").strip()
            if user_choice == "":
                print("No option selected.\n")
            elif user_choice in self.options:
                return user_choice
            else:
                for option in sorted(self.options): # Check if user typed in option instead of number
                    if user_choice.lower() in self.options[option].name.lower():
                        if yes_or_no(f"{self.options[option].name}?"):
                            return option
                        else:
                            continue
                else:
                    print(f"Sorry. I'm not sure what you mean by '{user_choice}'\n") 

class Leave_Mall:
    def __init__(self):
        self.name = "Leave Mall"
    
    def leave_mall(self):
        exit(0)

class Login_Register:
    def __init__(self):
        self.username = "User"
        self.password = "Password"