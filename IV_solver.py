from scipy.stats import norm
import mibian
'''http://www.codeandfinance.com/finding-implied-vol.html'''

n = norm.pdf
N = norm.cdf


'''Purely for IV bisection method with Merton Model as it has dividends

    Me([underlyingPrice, strikePrice, interestRate, annualDividends, \
			daysToExpiration], volatility=x, callPrice=y, putPrice=z)

	target_value = value of option
    S = Underlying Price
    K = Strike
    r = interest rate
    q = dividend
    v = implied volatility
    daystoexpiry = number of business days to expiration'''


def iv_newton(target_value, call_put, S, K, r, q, daystoexpiry):
    MAX_ITERATIONS = 50
    PRECISION = 1.0e-5
    sigma = 100
    for i in range(0, MAX_ITERATIONS):
        price, vega = bs_price(call_put, sigma, S, K, r, q, daystoexpiry)
        price = price
        diff = target_value - price  # target value is the market price, price is the option price given the sigma
        if (abs(diff) < PRECISION):
            return sigma
        if vega != 0:
            sigma = sigma + diff / vega  # f(x) / f'(x)
        else:
            return sigma
    # value wasn't found, return best guess so far
    return sigma

def bs_price(call_put, v, S, K, r, q, daystoexpiry):
    opt = mibian.Me([S, K, r, q, daystoexpiry], volatility=v)
    if call_put == 'call':
        return opt.callPrice, opt.vega
    else:
        return opt.putPrice, opt.vega


def iv_bisection(target_value, call_put, S, K, r, q, daystoexpiry):
    if call_put == 'call':
        opt = mibian.Me([S, K, r, q, daystoexpiry], callPrice=target_value)
    else:
        opt = mibian.Me([S, K, r, q, daystoexpiry], putPrice=target_value)
    return opt.impliedVolatility


def iv_solver(target_value, call_put, S, K, r, q, daystoexpiry):
    print([target_value, call_put, S, K, r, q, daystoexpiry])
    moneyness = K/S
    threshold = 1.0e-5
    try:
        newton = iv_newton(target_value, call_put, S, K, r, q, daystoexpiry)
        new_opt_error = abs(target_value - bs_price(call_put, newton, S, K, r, q, daystoexpiry)[0])
    except:
        newton = 0
        new_opt_error = abs(target_value)
    if new_opt_error < threshold:
        return newton
    elif moneyness > 0.9 and moneyness < 1.1:
        try:
            print('bisect')
            bisect = iv_bisection(target_value, call_put, S, K, r, q, daystoexpiry)
            bis_opt_error = abs(target_value - bs_price(call_put, bisect, S, K, r, q, daystoexpiry)[0])
        except:
            bisect = 0
            bis_opt_error = abs(target_value)
        if bis_opt_error < new_opt_error:
            return bisect
        else:
            return newton
    else:
        return 0

print(iv_solver(22.25, 'put', 156.79, 180.0, 0.01, 0.0, 7))