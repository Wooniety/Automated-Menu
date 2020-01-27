# Just utils stuff
import shutil
import hashlib
import bcrypt
from datetime import datetime
from os import system, name
from time import sleep

def if_num(num_to_check):
    """True or false if string is num(can be num or float)"""
    is_num = True
    try:
        if num_to_check.isnumeric():
            float(num_to_check)
        else:
            is_num = False
    except ValueError:
        is_num = False
    finally:
        return is_num

def to_num(int_to_check, error_msg = "Invalid number! Please enter something valid.\n", if_float = False, round_decimal = None):
    """String to num. Leave if_float empty if you want an int returned. Error msg also customizable """
    not_num = True
    while not_num:
        try:
            not_num = False
            if if_float:
                returned_num = float(int_to_check)
            else:
                returned_num = int(int_to_check)
        except ValueError:
            not_num = True
            int_to_check = input(f"{error_msg}")
        finally:
            if not not_num:
                if if_float and round_decimal != None:
                    returned_num = round(returned_num*(10**round_decimal))/(10**round_decimal)
                return returned_num

def yes_or_no(prompt, error_msg = None):
    """
    Prompts for Yes or No Question.\n
    print(f'{prompt} (Y/N): ')
    """
    while True:
        check = input(f"{prompt} (Y/N): ").strip()
        if check.lower() == "n" or check.lower() == "no":
            return False
        elif check.lower() == "y" or check.lower() == "yes":
            return True
        elif error_msg != None:
            print(error_msg)

def clear(): 
    """Clear Screen. Works for both Windows and Bash"""
    # Windows 
    if name == 'nt': 
        _ = system('cls') 
    # Bash
    else: 
        _ = system('clear') 

def get_day():
    """Return the day"""
    return datetime.today().strftime('%A')

def get_spaces(num_spaces):
    """Print spaces"""
    spaces = " " * num_spaces
    return spaces

def print_banner(section = "", msg = ""):
    """
    ***********************\n
    {Mall Name} - {section}\n
              {msg}\n
    ***********************
    """
    mall_name = "Krusty Krabz"
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    header = "*"*columns

    if section != "":
        mall_name = f"{mall_name} - {section}"
        header_spaces = get_spaces(int(columns/2-len(mall_name)/2))
    if msg != "":
        msg_spaces = get_spaces(int(columns/2 - len(msg)/2))
        mall_name = f"{mall_name}\n\n{msg_spaces}{msg}"

    banner = f"\033[1;36;40m{header}\n\n{header_spaces}{mall_name}\n\n{header}\033[0;37;40m"
    return banner

def enter_to_continue():
    """Usually to stop the screen from clearing"""
    input("\nPress Enter to continue... ")

def clear_cart():
    """Empty cart"""
    cart_file = open("data/cart.csv", "w")
    cart_file.write('"Items","Quantity","Price"')
    cart_file.close()

def valid_option(choice, num_of_options, option_zero = False):
    """Check if given option is correct. Choice is a string, num_of_options is an int. option_zero is True if there is an option zero."""
    if choice.isnumeric():
        choice = int(choice)
        if choice > num_of_options:
            return False
        elif option_zero and choice >= 0:
            return True
        elif choice >= 1:
            return True
        else:
            return False
    else:
        return False


def hashing(secret, salt):
    """Hash it in bcrypt"""
    return bcrypt.hashpw(secret, salt)

def send_bytes(string):
    """Send bytes"""