from statsmodels.tsa.ar_model import AutoReg
import numpy as np
from scipy.optimize import curve_fit
import src.helpers as helpers

def get_moving_average(window_size, prices):
    i = 0
    moving_average = []
    while i < (len(prices) - window_size):
        window_average = np.mean(prices[i:i+window_size])
        moving_average.append(window_average)
        i+=1
    return moving_average

def exponential_regression(x, y):
    popt, _ = curve_fit(helpers.exponential_func, x, y, p0=(1.0, 0.0), maxfev=10000)
    # Get the coefficients
    a, b = popt
    return a, b

# Fill weekends with linear interpolation (bad)
def fill_blanks(x, y):
    l = x[-1] + 1
    x, y = np.array(x), np.array(y)
    x_interp = np.arange(x[0], l)
    p_interp = np.interp(x_interp, x, y)
    return x_interp, p_interp

# Fill forward the last value (better)
def forward_fill(n, p):
    start = n[0]
    end = n[-1]

    length = end - start + 1

    n_vals = list(range(start, end + 1))
    p_vals = [0] * length

    # Fill in known values
    for idx, element in enumerate(n):
        p_vals[element - start] = p[idx]

    last_value = None
    for i in range(length):
        if p_vals[i] != 0:
            last_value = p_vals[i]
        else:
            if last_value is not None:
                p_vals[i] = last_value

    return n_vals, p_vals

    
def rm_exp_reg(p, a, b, length):
    p_norm = [0] * length
    for i in range(length):
        # p_norm[i] = x[i] - helpers.exponential_func(i, a, b)
        p_actual = p[i]
        p_expected = helpers.exponential_func(i, a, b)
        result = 100 * (p_actual - p_expected) / p_expected
        p_norm[i] = float(round( result, 3))
    return p_norm
    
# ARP model
def forecast_p_norm_arp(p_norm, length, _lags=5, horizon=10):
    model = AutoReg(p_norm, lags=_lags).fit()
    forecast = model.predict(start=length, end=length+horizon-1)
    return forecast



def forecast_p_norm_ma(p_norm, length, window=20, horizon=10):
    """
    Forecast p_norm using mean of last `window` values.
    """
    last = p_norm[-window:]
    mean_val = np.mean(last)
    return np.array([mean_val] * horizon).tolist()


def forecast_p_norm_ema(p_norm, length, alpha=0.2, horizon=10):
    """
    Forecast p_norm by exponential moving average.
    """
    ema = p_norm[0]
    for x in p_norm:
        ema = alpha * x + (1 - alpha) * ema
    return np.array([ema] * horizon).tolist()


def forecast_p_norm_seasonal(n, p_norm, horizon=10, period=5):
    """
    Forecast using seasonal average over last several cycles. 
    """
    forecasts = []
    for h in range(horizon):
        target_pos = (len(n) + h) % period

        # collect history of same weekday
        vals = [p_norm[i] for i in range(len(p_norm)) if i % period == target_pos]

        if len(vals) == 0:
            forecasts.append(0)
        else:
            forecasts.append(np.mean(vals))

    return np.array(forecasts)


# LITT FOR KOMPLISERT
# c, dx = 0, 0
# n, p = range(l), range(l)
# for i in range(l): p[i] = -1
# for i in range(l):
#     if i in x and not( p[i] == -1 ) :
#         p[i] = y[i]
#         continue
#     else:
#         if i < 1 or i > l: #not allowed
#             p[i] = -1
#         c = i
#         dx = 0
#         while c not in x and c < l:
#             c+=1
#             dx += 1
#         a = ( y[c] - y[i-1]) / dx
#         b = y[i-1]
#         for j in range(dx):
#             p[i] = a*j + b


        



