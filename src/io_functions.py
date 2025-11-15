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

def plotter(n, p, p_norm, Px=100, Py=100, price0=600, a=0.5, b=2, mode=10):

    t = np.linspace(0, 5000, 5000+1)

    fig, axs = plt.subplots(
        2, 1,
        sharex=True,
        gridspec_kw={'height_ratios': [5, 5]}
    )

    ma_lo_norm = analysis.get_moving_average(helpers.WINDOW_SIZE_LOWER, p_norm)
    ma_hi_norm = analysis.get_moving_average(helpers.WINDOW_SIZE_UPPER, p_norm)
    n_ma_lo = n[helpers.WINDOW_SIZE_LOWER::1]
    n_ma_hi = n[helpers.WINDOW_SIZE_UPPER::1]

    fig.set_size_inches((10, 8))

    axs[0].plot(n, p, color=helpers.COLOR_OSEBX, label="OSEBX Index")
    axs[0].scatter(Px, Py, color="red", label="Today")
    axs[0].grid(helpers.GRID_SHOW)
    axs[0].plot(t, helpers.exponential_func(t, a, b), color=helpers.COLOR_EXP_FUNC, label="Mean")

    axs[1].plot(n, p_norm, label="Price Normalized", color=helpers.COLOR_OSEBX_NORM)
    axs[1].scatter(Px, Py-helpers.exponential_func(Px, a, b), color="red")
    axs[1].axhline(0, color=helpers.COLOR_EXP_FUNC , linewidth="1.2")
    axs[1].plot(n_ma_lo, ma_lo_norm, label=f"MA {helpers.WINDOW_SIZE_LOWER}", color=helpers.COLOR_MA_LO)
    axs[1].plot(n_ma_hi, ma_hi_norm, label=f"MA {helpers.WINDOW_SIZE_UPPER}", color=helpers.COLOR_MA_HI)
    
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


