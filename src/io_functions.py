import src.helpers as helpers
import src.analysis as analysis
from src.modules import *

def startup():
    print_message("osebx.py")
    print_dotted_lines()
    print_ui()

def exit():
    print_message("qutting program")
    time.sleep(1)
    print_dotted_lines()

def inputter():
    available_modes = [10, 50]
    inp = get_input("<mode> <price>   >>> ")

    parts = inp.split()
    if len(parts) != 2:
        return None, None

    # Try converting to ints
    try:
        mode = int(parts[0])
        p_today = int(parts[1])
    except ValueError:
        return None, None

    # Validate mode
    if mode not in available_modes:
        return None, None

    return mode, p_today



def plotter(n, p, p_norm, Px=100, Py=100, price0=600, a=0.5, b=2, mode=10):

    t = np.linspace(0, helpers.N_CONT_TIME, helpers.N_CONT_TIME+1)

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
    axs[0].grid(helpers.SHOW_GRID)
    axs[0].plot(t, helpers.exponential_func(t, a, b), color=helpers.COLOR_EXP_FUNC, label="Mean")

    axs[1].plot(n, p_norm, label="Price Normalized", color=helpers.COLOR_OSEBX_NORM)
    axs[1].scatter(Px, Py-helpers.exponential_func(Px, a, b), color="red")
    axs[1].axhline(0, color=helpers.COLOR_EXP_FUNC , linewidth="1.2")
    axs[1].plot(n_ma_lo, ma_lo_norm, label=f"MA {helpers.WINDOW_SIZE_LOWER}", color=helpers.COLOR_MA_LO)
    axs[1].plot(n_ma_hi, ma_hi_norm, label=f"MA {helpers.WINDOW_SIZE_UPPER}", color=helpers.COLOR_MA_HI)
    
    plt.grid(helpers.SHOW_GRID)
    if helpers.SHOW_PLOT: plt.show()

def print_message(message):
     print()
     print(message)
     print()


def print_result(price, a, b):

    day = helpers.date_to_n( helpers.get_today_date() )
    price0 = helpers.date_to_n( helpers.START_DATE )

    advice = "None"
    expected_price = helpers.exponential_func(day, a, b)
    ratio = round((expected_price - price) / expected_price, 5)

    if -0.01 < ratio < 0.01: advice = "Neutral"
    if ratio < -0.01:        advice = "Sell"
    if ratio < -0.03:        advice = "Strong sell" 
    if ratio >  0.01:        advice = "Buy"
    if ratio >  0.03:        advice = "Strong buy" 

    print_delay()
    print_line()
    print_delay("Results")
    print_line()
    print_delay(f"~   Price0          ->  {price0}")
    print_delay(f"~   Current  price  ->  {price} ")
    print_delay(f"~   Expected price  ->  {int(expected_price)}")
    print_delay(f"~   Difference      ->  {round((ratio * -100), 3)} %")
    print_delay(f"~   Advice          ->  {advice}")
    print_delay()
    print_line()
    print_delay()

def print_ui():
    #ui print
    print_line()
    print_delay("Syntax        | Function" + " "*(helpers.CONSOLE_WIDTH-35)+f"Day: {helpers.days_since_start()}")
    print_line()
    print_delay("<enter>       : Quit")
    print_delay("<10> <price>  : 10 year (osebx)")
    print_delay("<50> <price>  : 10 year (sp500)")
    print_line()
    print_delay()

def print_delay(text = ""):
    time.sleep(helpers.DELAY)
    print(text)

def get_input(message):
    print()
    inp = input(message)
    print()
    return inp

def print_error(error):
    print()
    print(f"ERROR: {error}")
    print()

def print_dotted_lines():
    for i in range(helpers.VERTICAL_DOT_COUNT):
        print("   .")
        time.sleep(helpers.DELAY)
    print()

def print_line():
    print(helpers.CONSOLE_WIDTH * "-")


