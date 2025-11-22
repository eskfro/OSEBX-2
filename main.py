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
        if 1:
            mode, p_today = io_functions.inputter()
        elif 1:
            mode, p_today = 10, 1600
        else:
            mode, p_today = 50, 6580
            

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
            start_date = helpers.START_DATE
        elif mode == 50:
            file = helpers.FOLDER_SP500
            start_date = helpers.START_DATE_SP
        else:
            file = None
            io_functions.print_error("How")
            count += 1
            continue


        # Read data from file
        n, p, length = reader.read(file, start_date) 
        # modules.pprint.pprint(n[0:101]) 

        # modules.pprint.pprint(p[:-11:-1])


        # Update the status dictionary
        status["n_full"] = n[-1] == length - 1
        status["is_updated"] = helpers.date_to_n(helpers.get_today_date(), start_date) - 1 in n


        # Do analysis on the data
        a, b = analysis.exponential_regression(n, p)
        p_norm = analysis.rm_exp_reg(p, a, b, length)

        # Different forecast models
        p_norm_f_arp = analysis.forecast_p_norm_arp(p_norm, length, _lags=helpers.ARP_LAG, horizon=helpers.ARP_HORIZON)
        p_norm_f_ma = analysis.forecast_p_norm_ma(p_norm, length, window=helpers.MA_WINDOW, horizon=helpers.ARP_HORIZON)
        p_norm_f_ema = analysis.forecast_p_norm_ema(p_norm, length, alpha=helpers.EMA_ALPHA, horizon=helpers.ARP_HORIZON)
        p_norm_f_sea = analysis.forecast_p_norm_seasonal(n, p_norm, horizon=helpers.ARP_HORIZON, period=helpers.PERIOD_SEASONAL)


        # Transform the normalized plots to the normal one
        length_f = helpers.ARP_HORIZON
        p_f_arp = [0] * length_f
        p_f_ma = [0] * length_f
        p_f_ema = [0] * length_f
        p_f_sea = [0] * length_f

        for i in range(length_f):
            idx = n[-1] + 1 + i
            p_e = helpers.exponential_func(idx, a, b)
            p_f_arp[i] = p_e * (1 + p_norm_f_arp[i]/100) 
            p_f_ma[i] = p_e * (1 + p_norm_f_ma[i]/100) 
            p_f_ema[i] = p_e * (1 + p_norm_f_ema[i]/100) 
            p_f_sea[i] = p_e * (1 + p_norm_f_sea[i]/100) 


        # Calculate MA's
        ma_lo_norm = analysis.get_moving_average(helpers.WINDOW_SIZE_LOWER, p_norm)
        ma_hi_norm = analysis.get_moving_average(helpers.WINDOW_SIZE_UPPER, p_norm)

        ma_lo = [0] * (length - helpers.WINDOW_SIZE_LOWER) 
        ma_hi = [0] * (length - helpers.WINDOW_SIZE_UPPER)

        n_ma_lo = n[helpers.WINDOW_SIZE_LOWER::1]
        n_ma_hi = n[helpers.WINDOW_SIZE_UPPER::1]

        for i in range(length - helpers.WINDOW_SIZE_LOWER):
            idx = helpers.WINDOW_SIZE_LOWER + i
            p_e = helpers.exponential_func(idx, a, b)
            ma_lo[i] = p_e * (1 + ma_lo_norm[i]/100)

        for i in range(length - helpers.WINDOW_SIZE_UPPER):
            idx = helpers.WINDOW_SIZE_UPPER + i
            p_e = helpers.exponential_func(idx, a, b)
            ma_hi[i] = p_e * (1 + ma_hi_norm[i]/100)


        # Group data to be plotted
        p_norm_forecasts = {"arp" : p_norm_f_arp, "ma" : p_norm_f_ma, "ema" : p_norm_f_ema, "sea" : p_norm_f_sea }
        p_forecasts = {"arp" : p_f_arp, "ma" : p_f_ma, "ema" : p_f_ema, "sea" : p_f_sea }
        mas = {"n_ma_lo" : n_ma_lo, "n_ma_hi" : n_ma_hi, "ma_lo_norm" : ma_lo_norm, "ma_hi_norm" : ma_hi_norm, "ma_lo" : ma_lo, "ma_hi" : ma_hi}


        # Calculate forecast timeseries
        n_f_start = n[-1] + 1
        n_f_end = n_f_start + helpers.ARP_HORIZON
        n_f = range(n_f_start, n_f_end)


        # Plot / IO
        io_functions.plotter(n, p, p_norm, n_f, 
                             p_forecasts, p_norm_forecasts, 
                             mas, 
                             Px=helpers.date_to_n(helpers.get_today_date(), start_date), 
                             Py=p_today, 
                             length=length, a=a, b=b
                             )
        
        io_functions.print_result(p_today, a, b, status, start_date)

        count += 1

main()







