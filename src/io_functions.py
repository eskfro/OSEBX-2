import src.helpers as helpers
import src.analysis as analysis
from src.modules import *

def startup():
    print_message("osebx.py")
    print_dotted_lines()
    print_ui()

def exit():
    print_message("qutting program")
    time.sleep(1)
    print_dotted_lines()

def inputter():
    available_modes = [10, 50]
    inp = get_input("mode price   >>>   ")
    
    if inp in ["", " ", "exit"]:
        return -1, None

    parts = inp.split()
    if len(parts) != 2:
        return None, None

    # Try converting to ints
    try:
        mode = int(parts[0])
        p_today = int(parts[1])
    except ValueError:
        return None, None

    # Validate mode
    if mode not in available_modes:
        return None, None

    return mode, p_today




def print_message(message):
     print()
     print(message)
     print()




def print_ui():
    #ui print
    print_line()
    print_delay("Syntax        | Function" + " "*(helpers.CONSOLE_WIDTH-35))
    print_line()
    print_delay("10 price      : OSEBX")
    print_delay("50 price      : SP 500")
    print_line()
    print_delay()

def print_delay(text = ""):
    time.sleep(helpers.DELAY)
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
    for i in range(helpers.VERTICAL_DOT_COUNT):
        print("   .")
        time.sleep(helpers.DELAY)
    print()

def print_line():
    print(helpers.CONSOLE_WIDTH * "-")


