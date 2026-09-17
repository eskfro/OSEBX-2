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
        
        p_today = io_functions.get_user_input()
            
        # Handle input
        if p_today == -1: 
            return 0
        elif p_today is None:
            io_functions.print_error("Syntax Error")
            count += 1
            continue    
        elif p_today == "update":
            update_database_from_downloads()
            continue


        
        start_date = config.START_DATE_SP
        disp_name = config.DISP_NAME_SP
        
        n, p, length = database.get_timeseries()
        if p_today == ".":
            if length == 0:
                io_functions.print_error("No timeseries data available")
                count += 1
                continue
            p_today = int(p[-1])

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






