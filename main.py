import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions

def main():
    mode, p = io_functions.inputter()

    data = reader.reader(helpers.FOLDER_OSEBX)

    n, p = zip(*data)
    if mode == 10:
        io_functions.plotter(n, p)


main()







