# General config for this program
# Adjusted for linux right now
# Clone the repo into ~
# then set username

import datetime as dt

# --- user setup ---
FOLDER_USER = "/home/eskfro/"
FOLDER_DOWLOADS = FOLDER_USER + "Downloads/"

# --- Config for the diffferent modes ---
START_DATE = dt.datetime(2014, 5, 7)
DISP_NAME = "OSEBX"

START_DATE_SP = dt.datetime(2014, 7, 8)
DISP_NAME_SP = "SP-500"

FOLDER_OSEBX = FOLDER_USER + "OSEBX-2/data/osebx/"
FOLDER_SP500 = FOLDER_USER + "OSEBX-2/data/sp500/"
FOLDER_UPDATE_SOURCE_METADATA = FOLDER_USER + "OSEBX-2/data/db_update_sources.metadata"
DB_SP500 = FOLDER_USER + "OSEBX-2/data/timeseries_sp500.txt"

# Config mapping for the different modes
CONFIGS = {
    10 : (FOLDER_OSEBX, START_DATE, DISP_NAME),
    50 : (FOLDER_SP500, START_DATE_SP, DISP_NAME_SP)
}


# --- General ---
N_CONT_TIME = 5000

HY = 365//2
FY = 365

# --- IO ---
DELAY = 0.03
CONSOLE_WIDTH = 80
COLUMN_WIDTH_INDICATORS = 15
VERTICAL_DOT_COUNT = 5

SHOW_GRID = True
SHOW_PLOT = True

# --- Analysis ---
WINDOW_SIZE_LOWER = 50
WINDOW_SIZE_UPPER = 200

ARP_LAG = 900
ARP_HORIZON = 1200

MA_WINDOW = 200
EMA_ALPHA = 0.9
PERIOD_SEASONAL = 1200

# --- Colors ---
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