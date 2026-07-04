# This tool updates the data stored in the txt files.
# It identifies the downloaded file in the download folder and 

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config 
from src import csv_parser
from src import database
from src import helpers


def update_database_from_downloads():
    
    identifier_sp500 = "SP500F"
    identifier_extension = ".csv"

    download_dir = config.FOLDER_DOWLOADS

    if not os.path.isdir(download_dir):
        print(f"{download_dir} does not exist")
        return
    
    candidates = []
    for fn in os.listdir(download_dir):
        if not fn.startswith(identifier_sp500):
            continue
        if not fn.endswith(identifier_extension):
            continue 
        full = os.path.join(download_dir, fn)
        if os.path.isfile(full):
            candidates.append(full)

    if not candidates:
        print("Could not find source file for updating.")
        return

    # Newest matching file from download folder
    update_file = max(candidates, key=os.path.getmtime)
    print(f"Selected download: {update_file}")

    # TODO: check if filename already exist in "../data/db_update_sources.metadata"
    # if not exist append it to metadata and go throguth with the merge
    # else print already exist message

    seen_files = helpers.get_db_seen_files_metadata()
    source_name = os.path.basename(update_file)
    if source_name in seen_files:
        print(f"Update source already processed: {source_name}.")
        print("Aborting update.")
        return
    
    helpers.write_db_seen_files_metadata(source_name)

    n, p, length = csv_parser.create_timeseries_from_csv(update_file)

    database.append_and_merge_timeseries_to_db(n, p, length)

    print(f"Successfully updated database with {source_name}.")
    

if __name__ == "__main__":
    update_database_from_downloads()

