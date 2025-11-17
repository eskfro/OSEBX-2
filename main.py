import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis
import src.modules as modules

def main():
    c = 0
    while(1 and c == 0):
        mode, p_today = io_functions.inputter()
        mode, p_today = 10, 1615


        if mode == 10:
            file = helpers.FOLDER_OSEBX
        elif mode == 50:
            file = helpers.FOLDER_SP500
        else:
            return

        n, p = reader.read(file)
        l = len(n)
        print(l)
        modules.pprint.pprint(n[:-11:-1]) 
        modules.pprint.pprint(p[:-11:-1]) 
        a, b = analysis.exponential_regression(n, p)
        p_norm = analysis.rm_exp_reg(p, a, b, l)
        io_functions.plotter(n, p, p_norm, Px=helpers.days_since_start(), Py=p_today, a=a, b=b)

        c += 1

main()







