import src.legacy_parser as legacy_parser
import src.helpers as helpers
import src.io_functions as io_functions
import src.config as config
from src.dataobject import DataObject
import src.database as database

DEV = 1

def main():
    N = helpers.N_MAIN_LOOP
    if DEV: N = 1

    # Keep track of program state
    status = {
        "n_full" : False, 
        "is_updated": False
    }
    
    io_functions.startup()
    count = 0

    while(count < N):

        # Get input from user
        if not DEV:
            mode, p_today = io_functions.inputter()
        else:
            mode, p_today = 50, 7557
            
        # Handle input
        if mode == -1:
            return 0
        elif mode is None:
            io_functions.print_error("Syntax Error")
            count += 1
            continue    

        
        # Mode dependant configs
        file, start_date, disp_name = config.CONFIGS[mode]
        
        n, p, length = database.get_timeseries()

        # Init data object
        do = DataObject(n, p, length, status)
        do.integral_indicator_constants = (365//2, 365, 365+365//2, 2*365)
        do.start_date = start_date
        do.disp_name= disp_name
        do.Px = helpers.date_to_n(helpers.get_today_date(), start_date)
        do.Py = p_today

        # Data object functions
        do.analyze()
        do.create_integral_indicators()
        do.create_other_indicators()
        do.plot()
        do.print_results()
        
        count += 1
        

if __name__ == "__main__":
    main()







