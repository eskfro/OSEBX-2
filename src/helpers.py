import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config

import numpy as np
from datetime import datetime

def get_colored_string(text, color):
    return config.ANSI_TRANSLATOR[color] + text + config.ANSI_COLOR_RESET


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


def get_db_seen_files_metadata():
    seen_files = set()
    metadata = config.FOLDER_UPDATE_SOURCE_METADATA
    if not os.path.exists(metadata):
        print("Metadata file not found. Aborting update")
        return
    with open(metadata, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                seen_files.add(line)

    return seen_files
     
def write_db_seen_files_metadata(source_name):
    metadata = config.FOLDER_UPDATE_SOURCE_METADATA
    with open(metadata, "a", encoding="utf-8") as f:
        f.write(source_name + "\n")
     