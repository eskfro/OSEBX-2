import src.reader as reader
import src.helpers as helpers
import src.io_functions as io_functions
import src.analysis as analysis
import numpy as np
import matplotlib.pyplot as plt

class DataObject:
    def __init__(self, _n, _p, _length, _status):
        # Main arrays
        self.n = _n
        self.p = _p
        self.p_norm = None
        self.length = _length
        self.status = _status

        # Other constants
        self.start_date = None
        self.disp_name = None
        self.length_f = helpers.ARP_HORIZON
        self.a = None
        self.b = None
        self.Px = None
        self.Py = None

        # Normalized Prices forecast
        self.p_norm_f_arp = None
        self.p_norm_f_ma = None
        self.p_norm_f_ema = None
        self.p_norm_f_sea = None

        # Price forecasts
        self.p_f_arp = [0] * self.length_f
        self.p_f_ma = [0] * self.length_f
        self.p_f_ema = [0] * self.length_f
        self.p_f_sea = [0] * self.length_f

        # Movng average arrays
        self.ma_lo_norm = None
        self.ma_hi_norm = None
        self.ma_lo = [0] * (self.length - helpers.WINDOW_SIZE_LOWER) 
        self.ma_hi = [0] * (self.length - helpers.WINDOW_SIZE_UPPER)
        self.n_ma_lo = None
        self.n_ma_hi = None

        # Forecast n timeseries 
        self.n_f_start = None
        self.n_f_end = None
        self.n_f = None

        # Indicator list
        self.indicators = []
        self.integral_indicator_constants = None

    def int_indicator(self, numPastValues):
        N = numPastValues
        if len(self.p_norm) < N:
            return None
        
        pastValues = self.p_norm[-N:]

        integral = sum(pastValues)
        integral_avg = integral / numPastValues
        
        if integral > 0:
            return True, integral_avg
        else:
            return False, integral_avg

    def create_integral_indicators(self):
        for n in self.integral_indicator_constants:
            color = ""
            dispString = ""
            res, integral = self.int_indicator(n)

            if res is None:
                continue
            
            if res == False:
                color = "GREEN"
                dispString = "below"
            else:
                color = "RED"
                dispString = "above"

            ind = Indicator(f"int-{n}", dispString, 0.2, color, integral)
            self.indicators.append(ind)

    def create_other_indicators(self):
        # Indicators to be added
        currentPriceBelowMean = False
        color = "RED"
        dispString = "above"
        if self.p_norm[-1] < 0:
            currentPriceBelowMean = True
            color = "GREEN"
            dispString = "below"
        ind = Indicator("expectation", dispString, 0.2, color, None)

        self.indicators.append(ind)
        


    def analyze(self):
        # Update the status dictionary
        self.status["n_full"] = self.n[-1] == self.length - 1
        self.status["is_updated"] = helpers.date_to_n(helpers.get_today_date(), self.start_date) - 3 in self.n
        
        self.a, self.b = analysis.exponential_regression(self.n, self.p)
        self.p_norm = analysis.rm_exp_reg(self.p, self.a, self.b, self.length)

        # Normalized Prices forecast
        self.p_norm_f_arp = analysis.forecast_p_norm_arp(self.p_norm, self.length, _lags=helpers.ARP_LAG, horizon=helpers.ARP_HORIZON)
        self.p_norm_f_ma = analysis.forecast_p_norm_ma(self.p_norm, self.length, window=helpers.MA_WINDOW, horizon=helpers.ARP_HORIZON)
        self.p_norm_f_ema = analysis.forecast_p_norm_ema(self.p_norm, self.length, alpha=helpers.EMA_ALPHA, horizon=helpers.ARP_HORIZON)
        self.p_norm_f_sea = analysis.forecast_p_norm_seasonal(self.n, self.p_norm, horizon=helpers.ARP_HORIZON, period=helpers.PERIOD_SEASONAL)
        
        # Fill in price forecasts
        for i in range(self.length_f):
            idx = self.n[-1] + 1 + i
            p_e = helpers.exponential_func(idx, self.a, self.b)
            self.p_f_arp[i] = p_e * (1 + self.p_norm_f_arp[i]/100) 
            self.p_f_ma[i] = p_e * (1 + self.p_norm_f_ma[i]/100) 
            self.p_f_ema[i] = p_e * (1 + self.p_norm_f_ema[i]/100) 
            self.p_f_sea[i] = p_e * (1 + self.p_norm_f_sea[i]/100) 

        
        # Moving averages arrays
        self.ma_lo_norm = analysis.get_moving_average(helpers.WINDOW_SIZE_LOWER, self.p_norm)
        self.ma_hi_norm = analysis.get_moving_average(helpers.WINDOW_SIZE_UPPER, self.p_norm)
        self.n_ma_lo = self.n[helpers.WINDOW_SIZE_LOWER::1]
        self.n_ma_hi = self.n[helpers.WINDOW_SIZE_UPPER::1]
 
        # Transform normalized MA to real prices
        for i in range(self.length - helpers.WINDOW_SIZE_LOWER):
            idx = helpers.WINDOW_SIZE_LOWER + i
            p_e = helpers.exponential_func(idx, self.a, self.b)
            self.ma_lo[i] = p_e * (1 + self.ma_lo_norm[i]/100)

        for i in range(self.length - helpers.WINDOW_SIZE_UPPER):
            idx = helpers.WINDOW_SIZE_UPPER + i
            p_e = helpers.exponential_func(idx, self.a, self.b)
            self.ma_hi[i] = p_e * (1 + self.ma_hi_norm[i]/100)

        # Forecast n timeseries 
        self.n_f_start = self.n[-1] + 1
        self.n_f_end = self.n_f_start + helpers.ARP_HORIZON
        self.n_f = range(self.n_f_start, self.n_f_end)

    
    def plot(self):
        r_day = np.exp(self.b) - 1
        r_year = (1 + r_day)**365 - 1

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
        axs[0].set_title("Yearly growth: " + f"{round(r_year * 100, 2)}" + " %")
        axs[0].plot(self.n, self.p, color=helpers.COLOR_OSEBX, label=self.disp_name+" Index")
        axs[0].scatter(self.Px, self.Py, color="red", label="Today")
        axs[0].grid(helpers.SHOW_GRID)
        axs[0].plot(t, helpers.exponential_func(t, self.a, self.b), color=helpers.COLOR_EXP_FUNC, label="Mean")

        # Moving averages
        axs[0].plot(self.n_ma_lo, self.ma_lo, label=f"MA {helpers.WINDOW_SIZE_LOWER}", color=helpers.COLOR_MA_LO)
        axs[0].plot(self.n_ma_hi, self.ma_hi, label=f"MA {helpers.WINDOW_SIZE_UPPER}", color=helpers.COLOR_MA_HI)

        # Plot forecasts
        axs[0].plot(self.n_f, self.p_f_arp, label="ARP")
        #axs[0].plot(n_f, p_f_ma, label="MA")
        #axs[0].plot(n_f, p_f_ema, label="EMA")
        #axs[0].plot(n_f, p_f_sea, label="SEASONAL")

        Py_norm = 100 * (self.Py-helpers.exponential_func(self.Px, self.a, self.b)) / \
            helpers.exponential_func(self.Px, self.a, self.b)
        
        # Normalized plot
        axs[1].plot(self.n, self.p_norm, label=self.disp_name +" Index Normalized", color=helpers.COLOR_OSEBX_NORM)
        axs[1].scatter(self.Px, Py_norm, color="red", label="Today")
        axs[1].axhline(0, color=helpers.COLOR_EXP_FUNC , linewidth="1.2")
        axs[1].plot(self.n_ma_lo, self.ma_lo_norm, label=f"MA {helpers.WINDOW_SIZE_LOWER}", color=helpers.COLOR_MA_LO)
        axs[1].plot(self.n_ma_hi, self.ma_hi_norm, label=f"MA {helpers.WINDOW_SIZE_UPPER}", color=helpers.COLOR_MA_HI)

        # Plot normalized forecasts
        axs[1].plot(self.n_f, self.p_norm_f_arp, label="ARP")
        #axs[1].plot(n_f, p_norm_f_ma, label="MA")
        #axs[1].plot(n_f, p_norm_f_ema, label="EMA")
        #axs[1].plot(n_f, p_norm_f_sea, label="SEASONAL")

        # Plot integral indicator y-lines
        for integer in self.integral_indicator_constants:
            PosX = self.n[-1] - integer
            axs[1].axvline(PosX, color="blue", label=f"int-{integer}", linewidth=0.7)
        
        # X-Y limits
        scaler = 2
        dx = int( 300 )         * scaler
        dy = int( self.Py * 0.1 )    * scaler
        axs[0].set_xlim([self.Px-dx, self.Px+dx])
        axs[0].set_ylim([self.Py-dy, self.Py+dy])
        axs[0].legend()
        axs[1].set_xlim([self.Px-dx, self.Px+dx])
        axs[1].set_ylim([-25, 25])
        axs[1].legend()

        plt.grid(helpers.SHOW_GRID)

        if helpers.SHOW_PLOT:
            plt.show()
        
            
            
    def print_results(self):
       
        day = helpers.date_to_n(helpers.get_today_date(), self.start_date)
        expected_price = helpers.exponential_func(day, self.a, self.b)
        ratio = round((expected_price - self.Py) / expected_price, 5)

         

        # Status strings
        if (self.status["n_full"]): 
            nf = helpers.get_colored_string("True", "GREEN")
        else: 
            nf = helpers.get_colored_string("False", "RED")

        if (self.status["is_updated"]): 
            iu = helpers.get_colored_string("True", "GREEN")
        else: 
            iu = helpers.get_colored_string("False", "RED")

        io_functions.print_line()
        io_functions.print_delay(helpers.get_colored_string("Status List", "MAGENTA"))
        io_functions.print_line()
        io_functions.print_delay(f"->   n_full = {nf},   is_updated = {iu}")
        io_functions.print_line()
        io_functions.print_delay(helpers.get_colored_string("Price Difference", "MAGENTA"))
        io_functions.print_line()
        io_functions.print_delay(f"->   Price             =  {self.Py} ")
        io_functions.print_delay(f"->   Price (expected)  =  {int(expected_price)}")
        io_functions.print_delay(f"->   Difference        =  {round((ratio * -100), 3)} %")
        io_functions.print_delay()
        io_functions.print_line()
        io_functions.print_delay(helpers.get_colored_string("Indicators", "MAGENTA"))
        io_functions.print_line()
        

        # Print row explanation for indicators
        w = helpers.COLUMN_WIDTH_INDICATORS
        re = ["     "]
        io_functions.add_element_to_centered_strings(w, re, "indicator")
        io_functions.add_element_to_centered_strings(w, re, "meaning")
        io_functions.add_element_to_centered_strings(w, re, "weight")
        io_functions.add_element_to_centered_strings(w, re, "include")
        io_functions.add_element_to_centered_strings(w, re, "value %")
        row_explanation = helpers.get_colored_string("".join(re), "YELLOW")
        io_functions.print_delay(row_explanation)


        for ind in self.indicators:
            if isinstance(ind, Indicator):
                ind.print_indicator()


        

class Indicator:
    def __init__(self, _dispName, _dispString, _weight, _ansiColor, _integral):
        self.dispName = _dispName
        self.dispString = _dispString
        self.weight = _weight
        self.ansiColor = _ansiColor
        self.integral = _integral

        


    def print_indicator(self):

        def get_spacing_string(w, string):
            res = " " * (w - len(string))
            return res

        integral_string = " "
        try: 
            integral_string = f"{self.integral:.2f}"
        except Exception:
            integral_string = "na"

        ansiColor = self.ansiColor
        res = ""
        coloredDispString = helpers.get_colored_string(self.dispString, ansiColor)
        
        if self.ansiColor == "GREEN": advice = "1"
        else: advice = "0"
        
        # Column Width 
        w = helpers.COLUMN_WIDTH_INDICATORS
        
        # Creates a nice pattern depending on width w
        res += "->   "
        res += self.dispName + get_spacing_string(w, self.dispName)
        res += coloredDispString + get_spacing_string(w, self.dispString)
        res += str(round(self.weight, 2)) + get_spacing_string(w, str(round(self.weight, 2)))
        res += advice + get_spacing_string(w, advice)
        res += integral_string + get_spacing_string(w, integral_string)

        # Output
        io_functions.print_delay(res)


        
        


        
