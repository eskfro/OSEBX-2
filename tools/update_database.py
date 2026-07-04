# This tool updates the data stored in the txt files.
# It identifies the downloaded file in the download folder and 

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config 
from src import csv_parser
from src import database


def update_database_from_downloads():
    
    identifier_sp500 = "SP500F"
    identifier_extension = ".csv"

    target = config.DB_SP500

    path_downlads = os.Path(config.FOLDER_DOWLOADS)

    # TODO: find the newest file startting with identifie in the download folder.
    # then use the csv_parser to load the data into n, p, length. 

    # Newest matching file from download folder
    file_from_download_folder = ...

    n, p, length = csv_parser.create_timeseries_from_csv(file_from_download_folder)

    database.append_and_merge_timeseries_to_db(n, p, length)
    

if __name__ == "__main__":
    update_database_from_downloads()

