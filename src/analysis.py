from src.modules import *
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

