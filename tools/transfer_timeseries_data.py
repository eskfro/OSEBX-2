# TOOL
# The job of this file is to upload the old saved data
# stored in a collection of .txt files into a combined .db object. 
# The old data will later be deleted so mostly be one time use

import os
import sys
import datetime
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import legacy_parser
from src import config

# Tool to push data from old format to the new one
def transfer_timeseries_data():
    folder_path = "/home/eskfro/OSEBX-2/data/sp500"
    n, p, length = legacy_parser.read(folder_path, config.START_DATE_SP)

    upload_to_db(n, p, length)
    upload_to_txt(n, p, length)

    print("Transfer timeseries data completed")


def upload_to_txt(n, p, length):
    txt_obj = "timeseries_sp500_test.txt"
    txt_obj_folder = "/home/eskfro/OSEBX-2/data/"
    txt_path = os.path.join(txt_obj_folder, txt_obj)

    os.makedirs(txt_obj_folder, exist_ok=True)

    with open(txt_path, "w", encoding="utf-8") as f:
        for i in range(length):
            f.write(f"{n[i]} {p[i]}\n")

    print(f"Successfully wrote {length} records to {txt_path}")
    return True
    

# If db upload
def upload_to_db(n, p, length):
    # Load this into .db :
    # n : time samples (days)
    # p : price per time sample

    db_obj = "historical_data.db"
    db_obj_folder = "/home/eskfro/OSEBX-2/data/"
    db_path = os.path.join(db_obj_folder, db_obj)
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sp500_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert data
    try:
        for i in range(length):
            cursor.execute('''
                INSERT OR REPLACE INTO sp500_prices (date, price)
                VALUES (?, ?)
            ''', (n[i], p[i]))
        
        conn.commit()
        print(f"Successfully uploaded {length} records to {db_path}")
        return True
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    transfer_timeseries_data()