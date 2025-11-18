import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis
import src.modules as modules

def main():
    io_functions.startup()
    count = 0

    while(1 and count < 10):

        # Get input from user
        mode, p_today = io_functions.inputter()


        # Determine file depending on function
        if mode == 10:
            file = helpers.FOLDER_OSEBX
        elif mode == 50:
            file = helpers.FOLDER_SP500
        else:
            file = None
            return

        # Read data from file
        n, p, length = reader.read(file) 
        # modules.pprint.pprint(n[:-11:-1]) 
        # modules.pprint.pprint(p[:-11:-1]) 

        # Do analysis on the data
        a, b = analysis.exponential_regression(n, p)
        p_norm = analysis.rm_exp_reg(p, a, b, length)

        # Plot data and analysis
        io_functions.plotter(n, p, p_norm, Px=helpers.days_since_start(), Py=p_today, a=a, b=b)
        io_functions.print_result(p_today, a, b)

        count += 1

main()







