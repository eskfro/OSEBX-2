import src.helpers as helpers
import src.analysis as analysis
from src.modules import *

def startup():
    printMessage("osebx.py")
    printDottedLines()
    print_ui()

def exit():
    printMessage("qutting program")
    time.sleep(1)
    printDottedLines()

def inputter():
    return 10, 1600

def plotter(x, y):
    fig, axs = plt.subplots(2, 1)
    fig.set_size_inches((10, 8))

    axs[0].plot(x, y, color=helpers.COLOR_OSEBX)
    axs[0].grid(helpers.GRID_SHOW)

    plt.grid(helpers.GRID_SHOW)
    plt.show()

def printMessage(message):
     print()
     print(message)
     print()


def print_result(price, day, price0, a, b):
    advice = "None"
    expected_price = helpers.exponential_func(day, a, b)
    ratio = round((expected_price - price) / expected_price, 5)

    if -0.01 < ratio < 0.01: advice = "Neutral"
    if ratio < -0.01:        advice = "Sell"
    if ratio < -0.03:        advice = "Strong sell" 
    if ratio >  0.01:        advice = "Buy"
    if ratio >  0.03:        advice = "Strong buy" 

    printDelay()
    print_line()
    printDelay("Results")
    print_line()
    printDelay(f"~   Price0          ->  {price0}")
    printDelay(f"~   Current  price  ->  {price} ")
    printDelay(f"~   Expected price  ->  {int(expected_price)}")
    printDelay(f"~   Difference      ->  {round((ratio * -100), 3)} %")
    printDelay(f"~   Advice          ->  {advice}")
    printDelay()
    print_line()
    printDelay()

def print_ui():
    #ui print
    print_line()
    printDelay(f"Input       | Day: {helpers.days_since_date_new()}")
    print_line()
    printDelay()
    printDelay("[enter]     : Quit")
    printDelay("[0]         : Add    price data")
    printDelay("[1]         : Remove price data")
    printDelay("[10 price]  : 10 year (osebx)")
    printDelay("[50 price]  : 10 year (sp500)")
    printDelay()
    print_line()
    printDelay()

def printDelay(text = ""):
    time.sleep(helpers.DELAY)
    print(text)

def getInput(message):
    print()
    inp = input(message)
    print()
    return inp

def printError(error):
    print()
    print(f"ERROR: {error}")
    print()

def printDottedLines():
    for i in range(helpers.VERTICAL_DOT_COUNT):
        print("   .")
        time.sleep(helpers.DELAY)
    print()

def print_line():
    print(helpers.CONSOLE_WIDTH * "-")


