from src.modules import *

# Constants --------------------------------------------------


N_CONT_TIME = 5000

# IO stuff
DELAY = 0.03
CONSOLE_WIDTH = 120
COLUMN_WIDTH_INDICATORS = 15
VERTICAL_DOT_COUNT = 5

SHOW_GRID = True
SHOW_PLOT = True

# MA window sizes
WINDOW_SIZE_LOWER = 50
WINDOW_SIZE_UPPER = 200

# ANALYSIS
ARP_LAG = 500
ARP_HORIZON = 1200

MA_WINDOW = 200
EMA_ALPHA = 0.9
PERIOD_SEASONAL = 1200

# Colors
COLOR_OSEBX = "#f7a44a"
COLOR_OSEBX_NORM = "#f7a44a"
COLOR_EXP_FUNC = "#aa49e6"
COLOR_MA_LO = "#b47516"
COLOR_MA_HI = "#f00b0b"

ANSI_COLOR_RED = "\033[31m"
ANSI_COLOR_GREEN = "\033[32m"
ANSI_COLOR_BLUE = "\033[34m"
ANSI_COLOR_YELLOW = "\033[33m"
ANSI_COLOR_MAGENTA = "\033[35m"
ANSI_COLOR_CYAN = "\033[36m"
ANSI_COLOR_WHITE = "\033[37m"
ANSI_COLOR_RESET = "\033[0m"

ANSI_TRANSLATOR = {
     "RED" : ANSI_COLOR_RED,
     "GREEN" : ANSI_COLOR_GREEN,
     "BLUE" : ANSI_COLOR_BLUE,
     "WHITE" : ANSI_COLOR_WHITE,
     "YELLOW" : ANSI_COLOR_YELLOW,
     "MAGENTA" : ANSI_COLOR_MAGENTA,
     "CYAN" : ANSI_COLOR_CYAN
}


def get_colored_string(text, color):
    return ANSI_TRANSLATOR[color] + text + ANSI_COLOR_RESET


def get_today_date():
    today_date = datetime.today()
    formatted_date = today_date.strftime('%d.%m.%Y')
    return formatted_date

def exponential_func(x, a, b):
        return a * np.exp(b * x)

def date_to_n(date_type, start_date):
    if isinstance(date_type, str):
        date_type = datetime.strptime(date_type, "%d.%m.%Y")
    # this will be n in the array
    return (date_type - start_date).days


     