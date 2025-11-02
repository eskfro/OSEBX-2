from src.modules import *

# Constants --------------------------------------------------

FOLDER_OSEBX = "data_osebx/"
FOLDER_SP500 = "data_sp500/"
START_DATE = datetime(2014, 5, 7)

DELAY = 0.03
CONSOLE_WIDTH = 120
VERTICAL_DOT_COUNT = 5
WINDOW_SIZE_LOWER = 50
WINDOW_SIZE_UPPER = 200

GRID_SHOW = 1
COLOR_OSEBX = "blue"

# From old project --------------------------------------------

def get_today_date():
    today_date = datetime.today()
    formatted_date = today_date.strftime('%d.%m.%Y')
    return formatted_date

def exponential_func(x, a, b):
        return a * np.exp(b * x)

def days_since_start():
    return (datetime.now() - START_DATE).days

def date_to_n(date_type):
    if isinstance(date_type, str):
        date_type = datetime.strptime(date_type, "%d.%m.%Y")
    # this will be n in the array
    return (date_type - START_DATE).days

