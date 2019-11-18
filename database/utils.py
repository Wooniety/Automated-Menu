# Just utils stuff
import shutil
from datetime import datetime
from os import system, name
from time import sleep

def to_num(int_to_check, error_msg = None, if_float = False, round_decimal = None): #string to num. Leave if_float empty if you want an int returned. Error msg also customizable 
    not_num = True
    while not_num:
        try:
            not_num = False
            if not if_float:
                returned_num = int(int_to_check)
            else:
                returned_num = float(int_to_check)
        except ValueError:
            not_num = True
            if error_msg == None:
                int_to_check = input("Invalid number! Please enter something valid.\n") 
            else:
                int_to_check = input(f"{error_msg}")
        finally:
            if not not_num:
                if if_float and round_decimal != None:
                    returned_num = round(returned_num*(10**round_decimal))/(10**round_decimal)
                return returned_num

def yes_or_no(prompt, error_msg = None): # Prompt yes or no
    while True:
        check = input(f"{prompt} (Y/N): ").strip()
        if check.lower() == "n" or check.lower() == "no":
            return False
        elif check.lower() == "y" or check.lower() == "yes":
            return True
        elif error_msg != None:
            print(error_msg)

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux
    else: 
        _ = system('clear') 

def get_day(): # Return the day as a string
    return datetime.today().strftime('%A')

def print_banner(section = "", msg = ""): # Header banner
    mall_name = "Krusty Krabz"
    columns, rows = shutil.get_terminal_size(fallback=(80, 24))
    header = "*"*columns

    if section != "":
        mall_name = f"{mall_name} - {section}"
    header_spaces = " "*int(columns/2-len(mall_name)/2)
    if msg != "":
        msg_spaces = " "*int(columns/2 - len(msg)/2)
        mall_name = f"{mall_name}\n{msg_spaces}{msg}"

    banner = f"\033[1;36;40m{header}\n\n{header_spaces}{mall_name}\n\n{header}\033[0;37;40m"
    return banner

def enter_to_continue():
    input("\nPress Enter to continue... ")