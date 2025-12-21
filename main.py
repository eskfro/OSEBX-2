import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis
from src.DO import DataObject

def main():
    
    # Keep track of program state
    status = {
        "n_full" : False, 
        "is_updated": False
    }
    
    io_functions.startup()
    count = 0

    while(1 and count < 100):

        # Get input from user
        if 1:
            mode, p_today = io_functions.inputter()
        elif 1:
            mode, p_today = 10, 1600
        else:
            mode, p_today = 50, 6580
            
        # Handle input
        if mode == -1:
            return 0
        elif mode == None:
            io_functions.print_error("Syntax Error")
            count += 1
            continue    

        # Select constants depending on mode
        mode_selector = {
            10 : [helpers.FOLDER_OSEBX, helpers.START_DATE],
            50 : [helpers.FOLDER_SP500, helpers.START_DATE_SP]
        }
        selection = mode_selector[mode]
        file = selection[0]
        start_date = selection[1]
        
        # Read data from file
        n, p, length = reader.read(file, start_date) 
        do = DataObject(n, p, length, status)
        do.start_date = start_date
        do.Px = helpers.date_to_n(helpers.get_today_date(), start_date)
        do.Py = p_today
        do.analyze()
        do.plot()
        do.printResults()
        
        count += 1
        

if __name__ == "__main__":
    main()







