import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis
import src.modules as modules

def main():
    
    # Keep track of program state
    status = {
        "n_full" : False, 
        "is_updated": False
    }

    io_functions.startup()
    count = 0

    while(1 and count < 1):

        # Get input from user
        if 0:
            mode, p_today = io_functions.inputter()
        else:
            mode, p_today = 10, 1585
            

        # Handle input
        if mode == -1:
            return 0
        elif mode == None:
            io_functions.print_error("Syntax Error")
            count += 1
            continue    

        # Determine file depending on function
        if mode == 10:
            file = helpers.FOLDER_OSEBX
        elif mode == 50:
            file = helpers.FOLDER_SP500
        else:
            file = None
            io_functions.print_error("How")
            count += 1
            continue


        # Read data from file
        n, p, length = reader.read(file) 
        # modules.pprint.pprint(n[:-11:-1]) 
        # modules.pprint.pprint(p[:-11:-1])


        # Update the status dictionary
        status["n_full"] = n[-1] == length - 1 
        status["is_updated"] = helpers.days_since_start()-1 in n


        # Do analysis on the data
        a, b = analysis.exponential_regression(n, p)
        p_norm = analysis.rm_exp_reg(p, a, b, length)
        p_norm_f = analysis.forecast_p_norm(p_norm, length, _lags=helpers.ARP_LAG, horizon=helpers.ARP_HORIZON)

        n_f_start = n[-1] + 1
        n_f_end = n_f_start + helpers.ARP_HORIZON
        n_f = range(n_f_start, n_f_end)


        # Plot
        io_functions.plotter(n, p, p_norm, n_f, p_norm_f, Px=helpers.days_since_start(), Py=p_today, a=a, b=b)
        io_functions.print_result(p_today, a, b, status)

        count += 1

main()







