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

def yes_or_no(prompt, error_msg = None):
    while True:
        check = input(f"{prompt} (Y/N): ").strip()
        if check.lower() == "n" or check.lower() == "no":
            return False
        elif check.lower() == "y" or check.lower() == "yes":
            return True
        elif error_msg != None:
            print(error_msg)