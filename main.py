import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis

def main():
    c = 0
    while(1 and c == 0):
        mode, p = io_functions.inputter()
        mode, p = 50, 1600


        if mode == 10:
            file = helpers.FOLDER_OSEBX
        elif mode == 50:
            file = helpers.FOLDER_SP500
        else:
            return

        
        data = reader.read(file)
        n, p = zip(*data)
        n, p = analysis.fill_blanks(n[::-1], p[::-1])

        a, b = analysis.exponential_regression(n, p)
        io_functions.plotter(n, p, a=a, b=b)

        c += 1

main()







