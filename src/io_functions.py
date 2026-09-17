import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config.config as config
import time

def startup():
    print_message("osebx.py")
    print_dotted_lines()
    print_ui()

def exit():
    print_message("qutting program")
    time.sleep(1)
    print_dotted_lines()

def get_user_input():
    inp = get_input("price   >>>   ")
    
    if inp in ["", " ", "exit"]:
        return -1
    
    if inp == "update":
        return "update"
    
    if inp == ".":
        return "."

    try:
        p_today = int(inp)
    except ValueError:
        return None

    return p_today




def print_message(message):
     print()
     print(message)
     print()


def add_element_to_centered_strings(w, string_list, string_to_add):
    string_list.append(string_to_add + get_spacing_string(w, string_to_add))

def get_spacing_string(w, string):
    res = " " * (w - len(string))
    return res


def print_ui():
    #ui print
    print_line()
    print_delay("Syntax        | Function" + " "*(config.CONSOLE_WIDTH-35))
    print_line()
    print_delay("price         : SP 500")
    print_delay(".             : Use latest SP 500 value")
    print_line()
    print_delay()

def print_delay(text = ""):
    time.sleep(config.DELAY)
    print(text)

def get_input(message):
    print()
    inp = input(message)
    print()
    return inp

def print_error(error):
    print()
    print(f"ERROR: {error}")
    print()

def print_dotted_lines():
    for i in range(config.VERTICAL_DOT_COUNT):
        print("   .")
        time.sleep(config.DELAY)
    print()

def print_line():
    print(config.CONSOLE_WIDTH * "-")

