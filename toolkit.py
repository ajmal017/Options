import questrade_data

session = questrade_data.sess

'''Ticker must be a string; preferably this ticker should be the base
ex. print(get_underlying_internal_code('RY'))
'''
def get_underlying_internal_code(ticker):
    ticker_finder = session.get_symbols_search(prefix=ticker).get('symbols')
    undl_code=0
    for i in range(len(ticker_finder)):
        if ticker_finder[i].get('symbol') == ticker:
            undl_code = ticker_finder[i].get('symbolId')
    return undl_code
#
# print(get_underlying_internal_code('RY'))