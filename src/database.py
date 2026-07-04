# Safely update the txt database
# Merge incoming data with the existing data
# The existing is prioritized if for any reason there would be differences   

# db format
# n, p
# 0	1961.0000
# 1	1967.0000
# 2	1958.0000
# 3	1963.0000
# ...

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from config import config

def validate_line(line):
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    fields = line.split()
    if len(fields) < 2:
        return None
    try:
        day = int(fields[0])
        price = float(fields[1].replace(",", "."))
    except ValueError:
        return None
    return day, price

def get_timeseries():
    db = config.DB_SP500
    days = []
    prices = []

    if not os.path.exists(db):
        print("Database does not exist.")
        return np.array([], dtype=int), np.array([], dtype=float), 0

    with open(db, "r", encoding="utf-8") as f:
        for line in f:
            valid = validate_line(line)
            if valid is None:
                continue
            day, price = valid
            days.append(day)
            prices.append(price)

    n = np.array(days, dtype=int)
    p = np.array(prices, dtype=float)

    return n, p, len(n)


def append_and_merge_timeseries_to_db(n, p, length):
    # The incoming timeseries most likely have some overlap.
    db_path = config.DB_SP500
    existing = {}
    
    if not os.path.exists(db_path):
        print(f"Database file does not exist: {db_path}")
        return

    # Open the db file which is a txt file (see data/timeseries_sp500)
    with open(db_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if line.startswith("#"):
                continue
            fields = line.split()
            if len(fields) < 2:
                continue

            try:
                day = int(fields[0])
                price = float(fields[1].replace(",", "."))
            except ValueError as e:
                print(e)
                continue

            # Add db data to existing
            if day not in existing:
                existing[day] = price

    for i in range(length):
        try:
            day = int(n[i])
            price = float(p[i])
        except (ValueError, TypeError) as e:
            print(e)
            continue
        
        # Add ts data to existing
        if day not in existing:
            existing[day] = price

    # Write new data
    with open(db_path, "w", encoding="utf-8") as f:
        for day in sorted(existing):
            f.write(f"{day}\t{existing[day]:.4f}\n")
