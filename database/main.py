# Import the other files
from common_menu import *

def main():
    print("Hi this is the Krusty Krab Shopping Mart. Mr Krabs lost Spongebob and couldn't continue running the other one so he started a shopping mall to overcome his depression.")
    main_menu = Menu("0", "Leave the mall",
                    "1", "Login/Register",
                    "2", "Get a shopping cart/basket", 
                    "3", "Explore the shopping aisle", 
                    "4", "Search for specific item", 
                    "5", "Head to the cashier")
    choice = main_menu.show_menu()

main()