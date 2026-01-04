import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis
from src.DO import DataObject

DEV = 1
N_MAIN_LOOP = 100

def main():
    if DEV: N_MAIN_LOOP = 1

    # Keep track of program state
    status = {
        "n_full" : False, 
        "is_updated": False
    }
    
    io_functions.startup()
    count = 0

    while(count < N_MAIN_LOOP):

        # Get input from user
        if not DEV:
            mode, p_today = io_functions.inputter()
        else:
            mode, p_today = 10, 1700
            
        # Handle input
        if mode == -1:
            return 0
        elif mode is None:
            io_functions.print_error("Syntax Error")
            count += 1
            continue    

        # Config selector
        configs = {
            10 : (helpers.FOLDER_OSEBX, helpers.START_DATE, helpers.DISP_NAME),
            50 : (helpers.FOLDER_SP500, helpers.START_DATE_SP, helpers.DISP_NAME_SP)
        }
        config = configs[mode]
        
        file, start_date, disp_name = config
        
        # Read data from file
        n, p, length = reader.read(file, start_date) 

        # Init data object
        do = DataObject(n, p, length, status)
        do.integral_indicator_constants = (365//2, 365, int(1.5*365), 2*365)
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







