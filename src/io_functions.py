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
    inp = get_input("mode price   >>>   ")
    
    if inp in ["", " ", "exit"]:
        return -1, None

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




def plotter(n, p, p_norm, n_f, p_forecasts, p_norm_forecasts, 
            mas, Px=100, Py=100, length=0, a=0.5, b=2):

    p_norm_f_arp = p_norm_forecasts["arp"]
    p_norm_f_ma = p_norm_forecasts["ma"]
    p_norm_f_ema = p_norm_forecasts["ema"]
    p_norm_f_sea = p_norm_forecasts["sea"]

    p_f_arp = p_forecasts["arp"]
    p_f_ma = p_forecasts["ma"]
    p_f_ema = p_forecasts["ema"]
    p_f_sea = p_forecasts["sea"]

    n_ma_lo = mas["n_ma_lo"]
    n_ma_hi = mas["n_ma_hi"]
    ma_lo_norm = mas["ma_lo_norm"]
    ma_hi_norm = mas["ma_hi_norm"]
    ma_lo = mas["ma_lo"]
    ma_hi = mas["ma_hi"]


    # Time cont. time
    t = np.linspace(0, helpers.N_CONT_TIME, helpers.N_CONT_TIME+1)

    # Figure
    fig, axs = plt.subplots(
        2, 1,
        sharex=True,
        gridspec_kw={'height_ratios': [5, 5]}
    )
    fig.set_size_inches((10, 8))

    # Growth plot
    axs[0].plot(n, p, color=helpers.COLOR_OSEBX, label="OSEBX Index")
    axs[0].scatter(Px, Py, color="red", label="Today")
    axs[0].grid(helpers.SHOW_GRID)
    axs[0].plot(t, helpers.exponential_func(t, a, b), color=helpers.COLOR_EXP_FUNC, label="Mean")

    # Moving averages
    axs[0].plot(n_ma_lo, ma_lo, label=f"MA {helpers.WINDOW_SIZE_LOWER}", color=helpers.COLOR_MA_LO)
    axs[0].plot(n_ma_hi, ma_hi, label=f"MA {helpers.WINDOW_SIZE_UPPER}", color=helpers.COLOR_MA_HI)

    # Plot forecasts
    axs[0].plot(n_f, p_f_arp, label="ARP")
    #axs[0].plot(n_f, p_f_ma, label="MA")
    #axs[0].plot(n_f, p_f_ema, label="EMA")
    axs[0].plot(n_f, p_f_sea, label="SEASONAL")



    Py_norm = 100 * (Py-helpers.exponential_func(Px, a, b)) / helpers.exponential_func(Px, a, b)
    # Normalized plot
    axs[1].plot(n, p_norm, label="OSEBX Index Normalized", color=helpers.COLOR_OSEBX_NORM)
    axs[1].scatter(Px, Py_norm, color="red", label="Today")
    axs[1].axhline(0, color=helpers.COLOR_EXP_FUNC , linewidth="1.2")
    axs[1].plot(n_ma_lo, ma_lo_norm, label=f"MA {helpers.WINDOW_SIZE_LOWER}", color=helpers.COLOR_MA_LO)
    axs[1].plot(n_ma_hi, ma_hi_norm, label=f"MA {helpers.WINDOW_SIZE_UPPER}", color=helpers.COLOR_MA_HI)

    # Plot normalized forecasts
    axs[1].plot(n_f, p_norm_f_arp, label="ARP")
    #axs[1].plot(n_f, p_norm_f_ma, label="MA")
    #axs[1].plot(n_f, p_norm_f_ema, label="EMA")
    axs[1].plot(n_f, p_norm_f_sea, label="SEASONAL")
    
    # X-Y limits
    scaler = 2
    dx = int( 300 )         * scaler
    dy = int( Py * 0.1 )    * scaler
    axs[0].set_xlim([Px-dx, Px+dx])
    axs[0].set_ylim([Py-dy, Py+dy])
    axs[0].legend()
    axs[1].set_xlim([Px-dx, Px+dx])
    axs[1].set_ylim([-25, 25])
    axs[1].legend()

    plt.grid(helpers.SHOW_GRID)
    if helpers.SHOW_PLOT: plt.show()



def print_message(message):
     print()
     print(message)
     print()


def print_result(price, a, b, status, start_date):

    day = helpers.date_to_n(helpers.get_today_date(), start_date)
    expected_price = helpers.exponential_func(day, a, b)
    ratio = round((expected_price - price) / expected_price, 5)

    # Determine advice
    advice = "None"
    if -0.01 < ratio < 0.01: advice = "Neutral"
    if ratio < -0.01:        advice = "Sell"
    if ratio < -0.03:        advice = "Strong sell" 
    if ratio >  0.01:        advice = "Buy"
    if ratio >  0.03:        advice = "Strong buy" 

    # Status strings
    if (status["n_full"]): 
        nf = helpers.get_colored_string("True", "GREEN")
    else: 
        nf = helpers.get_colored_string("False", "RED")

    if (status["is_updated"]): 
        iu = helpers.get_colored_string("True", "GREEN")
    else: 
        iu = helpers.get_colored_string("False", "RED")



    print_delay()
    print_line()
    print_delay(f"Results                                               n_full = {nf}          is_updated = {iu}")
    print_line()
    print_delay(f"->   Price             =  {price} ")
    print_delay(f"->   Price (expected)  =  {int(expected_price)}")
    print_delay(f"->   Difference        =  {round((ratio * -100), 3)} %")
    print_delay(f"->   Advice            =  {advice}")
    print_delay()
    print_line()
    print_delay()

def print_ui():
    #ui print
    print_line()
    print_delay("Syntax        | Function" + " "*(helpers.CONSOLE_WIDTH-35))
    print_line()
    print_delay("10 price      : OSEBX")
    print_delay("50 price      : SP 500")
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


