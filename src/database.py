# Safely update the txt database
# Merge incoming data with the existing data
# The existing is prioritized if for any reason there would be differences   

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config


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
