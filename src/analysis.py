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


def fill_blanks(x, y):
    l = x[-1] + 1
    x, y = np.array(x), np.array(y)
    x_interp = np.arange(x[0], l)
    p_interp = np.interp(x_interp, x, y)
    return x_interp, p_interp

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


        



