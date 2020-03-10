import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")

# print(msft.info)
# msft.calendar
# print(msft.options[1])
# opt = msft.option_chain('2019-11-28')
# print(opt.calls.columns.values.tolist())

col_list = ['contractSymbol','strike', 'lastPrice', 'bid', 'ask', 'change', 'percentChange', 'volume', 'openInterest', 'impliedVolatility', 'inTheMoney','Moneyness']


def options_chain_scrap(ticker,callput,date):
    ticker = yf.Ticker(ticker)
    cur_data = ticker.history(start = date,end=date)
    opt_exp_list = ticker.options[:5]
    storage = pd.DataFrame()
    for i in opt_exp_list:
        if callput == 'C':
            opt_store= ticker.option_chain(i).calls
        else:
            opt_store= ticker.option_chain(i).puts
        storage=pd.concat([storage,opt_store])
    storage.fillna(0,inplace=True)
    # print(cur_data['Close'].values)
    storage['Spot Price'] = cur_data['Close'].values[0]
    storage['Moneyness'] = ((storage['strike']/storage['Spot Price']).round(2)*100).astype(str) + '%'
    storage = storage[col_list]
    return storage

# def price_hist_data(ticker):

#
print(options_chain_scrap('AAPL', 'C','2019-11-22'))
## TESTS