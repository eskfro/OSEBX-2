import datetime as dt

# --- user setup ---
FOLDER_USER = "/home/eskfro/"
FOLDER_DOWLOADS = FOLDER_USER + "Downloads/"



# --- config for the diffferent modes ---
START_DATE = dt.datetime(2014, 5, 7)
DISP_NAME = "OSEBX"

START_DATE_SP = dt.datetime(2014, 7, 8)
DISP_NAME_SP = "SP-500"

FOLDER_OSEBX = FOLDER_USER + "OSEBX-2/data/osebx/"
FOLDER_SP500 = FOLDER_USER + "OSEBX-2/data/sp500/"
FOLDER_UPDATE_SOURCE_METADATA = FOLDER_USER + "OSEBX-2/data/db_update_sources.metadata"

# TODO: change the file name after testing is done
DB_SP500 = FOLDER_USER + "OSEBX-2/data/timeseries_sp500.txt"

# Config mapping for the different modes
CONFIGS = {
    10 : (FOLDER_OSEBX, START_DATE, DISP_NAME),
    50 : (FOLDER_SP500, START_DATE_SP, DISP_NAME_SP)
}
