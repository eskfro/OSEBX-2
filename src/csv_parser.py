# Input: file to parse
# Ouput:
# n: np.array
# p: np.array
# length: int

# Input csv format: 

#Dato	Åpning	Høy	Lav	Sluttkurs	Antall
#01.07.2026	7543	7579	7506	7535	1258081
#30.06.2026	7496	7568	7482	7548	1217536
#28.06.2026	7398	7505	7398	7500	1400892

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

use_forward_fill = True

from config import config
from src import helpers
import numpy as np
import os

def line_ok(line):
    if not line:
        return False
    if line.startswith("#"):
        return False
    if line.lower().startswith("dato"):
        return False
    
    return True

def create_timeseries_from_csv(file):
    days = []
    prices = []
    # n[i] = field number 0
    # p[i] = field number 4
    with open(file, encoding="utf-16") as f:
        # If we choose to use forward fill we
        # must record the last n.
        prev_day = None
        prev_price = None
        for line in f:
            line = line.strip()
            if not line_ok(line):
                continue

            fields = line.split()
            if len(fields) < 2:
                continue
            date = fields[0]

            # Sometimes one price is missing in the data
            if len(fields) < 5: 
                price_index = 2
            else:
                price_index = 4
            if price_index > len(fields):
                continue 
            price_string = fields[price_index].replace(",", ".")

            # Convert to float
            try:
                price = float(price_string)
            except ValueError as e:
                print(e)
                continue
            
            # Convert to day number
            try:
                day = helpers.date_to_n(date, config.START_DATE_SP)
            except ValueError as e:
                print(e)
                continue

            # Forward fill will break frequency decomposition 
            # but thats ok
            if use_forward_fill:

                if prev_day == None:
                    days.append(day)
                    prices.append(price)
                    prev_day, prev_price = day, price
                    continue

                missing_days = prev_day - 1 - day 
                
                # Fill the missing days
                for i in range(missing_days):
                    prev_day -= 1
                    days.append(prev_day)
                    prices.append(price)

            prev_day = day
            prev_price = price
            days.append(day)
            prices.append(price)

    n = np.array(days[::-1], dtype=int)
    p = np.array(prices[::-1], dtype=float)
    length = len(n)

    return n, p, length
                

def create_timeseries_from_csv_test():

    file = "/home/eskfro/Downloads/SP500F_05.07.2016--01.07.2026.csv"

    n, p, length = create_timeseries_from_csv(file)

    for i in range(length-1):
        print(n[i], "  ", p[i])
        quit = False
        if n[i] > n[i+1]:
            print(f"Test not passed: n incrementing fault 1 @ index = {i}")
            quit = True
        if use_forward_fill and ( n[i]+1 != n[i+1] ):
            print(f"Test not passed: n incrementing fault 2 @ index = {i}")
            quit = True

        try:
            p_float = float(p[i])
            if p_float < 1.0:
                print("Test not passed: float( p[i] ) < 1")
        except ValueError as e:
            print(e)
            quit = True
        
        if quit:
            print("Quitting test")
            return

    print("All tests passed")

if __name__ == "__main__":
    create_timeseries_from_csv_test()