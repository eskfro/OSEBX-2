#!/usr/bin/env python3
import src.legacy_parser as legacy_parser
import src.helpers as helpers
import src.io_functions as io_functions
import config.config as config
from src.dataobject import DataObject
from tools.update_database import update_database_from_downloads
import src.database as database

def main():

    program_status = {
        "n_full" : False, 
        "is_updated": False
    }
    
    io_functions.startup()

    count, max_iter = 0, 10
    while(count < max_iter):

        # Get input from user
        
        mode, p_today = io_functions.get_user_input()
            
        # Handle input
        if mode == -1: 
            return 0
        elif mode is None:
            io_functions.print_error("Syntax Error")
            count += 1
            continue    
        elif mode == "update":
            update_database_from_downloads()
            continue

        # Mode dependant configs
        file, start_date, disp_name = config.CONFIGS[mode]
        
        n, p, length = database.get_timeseries()

        # Init data object
        do = DataObject(n, p, length, program_status)
        do.integral_indicator_constants = (1*365, 2*365, 3*365, 4*365)
        do.start_date = start_date
        do.disp_name= disp_name
        do.Px = helpers.date_to_n(helpers.get_today_date(), start_date)
        do.Py = p_today

        # Data object functions
        do.timeseries_analysis()
        do.create_integral_indicators()
        do.create_indicators()
        do.print_results()
        do.plot()
        
        count += 1
        

if __name__ == "__main__":
    main()







