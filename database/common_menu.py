from macros import *

class Menu:
    def __init__(self, *options):
        self.options = {}
        for i in range(0, len(options), 2):
            self.options[options[i]] = options[i+1] 

    def show_menu(self):
        while True:
            for option in sorted(self.options):
                print(f"{option}) {self.options[option]}")
            user_choice = input("Please enter an option: ").strip()
            if user_choice == "":
                print("No option selected.\n")
            elif user_choice in self.options:
                return user_choice
            else:
                for option in sorted(self.options): # Check if user typed in option instead of number
                    if user_choice.lower() in self.options[option].lower():
                        if yes_or_no(f"{self.options[option]}?"):
                            return option
                        else:
                            continue
                else:
                    print(f"Sorry. I'm not sure what you mean by '{user_choice}'\n")                

class Login_Register:
    def __init__(self):
        self.username = "Henggy"
        self.password = "Password"

class Items_For_Sale:
    def __init__(self, item, price, stock):
        self.item = item
        self.price = price
        self.stock = stock