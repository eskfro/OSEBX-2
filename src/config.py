from datetime import datetime

WIN_USERNAME = "ESKFR"
FOLDER_OSEBX = "C:\\Users\\" + WIN_USERNAME + "\\OSEBX-2\\data_osebx"
FOLDER_SP500 =  "C:\\Users\\" + WIN_USERNAME + "\\OSEBX-2\\data_sp500"
START_DATE = datetime(2014, 5, 7)
START_DATE_SP = datetime(2014, 7, 8)
DISP_NAME = "OSEBX"
DISP_NAME_SP = "SP-500"

LINUX = True

if LINUX:
    FOLDER_OSEBX = "/home/eskfro/OSEBX-2/data/osebx"
    FOLDER_SP500 = "/home/eskfro/OSEBX-2/data/sp500"

CONFIGS = {
    10 : (FOLDER_OSEBX, START_DATE, DISP_NAME),
    50 : (FOLDER_SP500, START_DATE_SP, DISP_NAME_SP)
}