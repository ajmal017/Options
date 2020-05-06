import pandas as pd
import datetime
import IV_solver as iv
import utils as u

'''To initialize, run the following code:
from questrade_api import Questrade
t='lbM7LwESNm8rXnx5zxJ8r-6f_-9JExT30'
q = Questrade(grant_type=t, refresh_token=t)
import data as d
'''

# cols = ['symbol', 'strike', 'Expiry', 'CallPut', 'bidPrice', 'askPrice', 'lastTradePrice', 'openPrice', 'volume',
#         'openInterest', 'delta', 'gamma', 'vega', 'theta', 'moneyness', 'Days to Expiry', 'IV','delta_opt', 'gamma_opt', 'vega_opt', 'theta_opt']

cols = ['symbol', 'strike', 'Expiry', 'CallPut', 'bidPrice', 'askPrice', 'lastTradePrice', 'openPrice', 'volume',
        'openInterest', 'delta', 'gamma', 'vega', 'theta', 'moneyness', 'Days to Expiry', 'IV']

today = datetime.datetime.today().date()

'''Returns a symbol id for a given ticker; code below is used to ensure that it is unique for each ticker'''


def retrieve_positions(q):
    acc_num = q.accounts['accounts'][0]['number']
    positions = q.account_positions(acc_num)['positions']
    position_df = pd.DataFrame(positions)
    return list(position_df['symbolId'])


def retrieve_orders(q):
    acc_num = q.accounts['accounts'][0]['number']
    positions = q.account_orders(acc_num,startTime='2020-04-10T00:00:00-0')['orders']
    position_df = pd.DataFrame(positions)
    position_df = position_df[position_df['state'] == 'Accepted']
    position_df = position_df[['symbol', 'symbolId', 'side', 'limitPrice']].set_index(('symbol'))
    return position_df


def extract_symbolid(q, ticker):
    access_dict = q.symbols_search(prefix=ticker)['symbols']
    total_len = len(access_dict)
    symbol_id = []
    for i in range(total_len):
        if (access_dict[i]['isTradable'] == True) and (access_dict[i]['isQuotable'] == True):
            if access_dict[i]['symbol'] == ticker:
                symbol_id.append((ticker, access_dict[i]['symbolId']))
    if len(symbol_id) == 1:
        return symbol_id[0][1]
    else:
        return symbol_id


def retrieve_mult_symbolid(q, alistticker):
    newlist = []
    for i in alistticker:
        new_ticker = extract_symbolid(q, i)
        if new_ticker != []:
            newlist.append(new_ticker)
    return newlist


'''alist is either a list of tickers (in the case that sym_list is False or a list of symids
    Returns: Dataframe of bid, ask, last, open, and pct change sorted
    '''


def retrieve_symbolid_list(q, df, alist = False):
    if alist:
        sym_list = retrieve_mult_symbolid(q, df)
    else:
        sym_list = list(df['symbolId'])
    ticker_string = str(sym_list)[1:-1]
    quote = q.markets_quotes(ids=ticker_string)['quotes']
    df_live = pd.DataFrame(quote)[['symbol', 'bidPrice', 'askPrice', 'lastTradePrice', 'openPrice']].set_index('symbol')
    if not alist:
        merge_df = df_live.merge(df, how='inner', left_index=True, right_index=True)
        final_df = merge_df
        final_df['pct_chg'] = ((merge_df['lastTradePrice'] / merge_df['openPrice']) - 1)
    else:
        final_df = df_live
        final_df['pct_chg'] = ((df_live['lastTradePrice'] / df_live['openPrice']) - 1)
    if not alist:
        final_df['abs_limit'] = abs(merge_df['lastTradePrice']-merge_df['limitPrice'])
        final_df['pct_limit'] = abs(merge_df['limitPrice']/merge_df['lastTradePrice'] - 1)
    return final_df


'''Returns a dataframe with each ticker's option codes for each expiry and its strike'''

def extract_opt_data(q, ticker, date_lim='all', bod=False):
    symbol_id = extract_symbolid(q, ticker)
    cur_price, cur_yield = get_price_yield(q, ticker, bod)
    opt_chain_ids = q.symbol_options(symbol_id)['optionChain']
    count = len(opt_chain_ids) - 1
    if (date_lim != 'all') and count > date_lim:
        count = date_lim
    df = pd.DataFrame(columns=['strikePrice', 'callSymbolId', 'putSymbolId', 'Expiry'])
    for i in range(count):
        exp_date = opt_chain_ids[i]['expiryDate'][:10]
        exp_set = opt_chain_ids[i]['chainPerRoot'][0]['chainPerStrikePrice']
        df_insert = pd.DataFrame(exp_set)
        df_insert['Expiry'] = exp_date
        df = df.append(df_insert)
    df['moneyness'] = df['strikePrice'].apply(lambda x: float(x) / float(cur_price))
    df = df[(df['moneyness'] >= 0.75) & (df['moneyness'] <= 1.25)]
    df.columns = ['Strike', 'Call Code', 'Put Code', 'Expiry', 'Moneyness']
    return df


def get_price_yield(q, ticker, bod=False):
    sym_id = extract_symbolid(q, ticker)
    cur_price_data = q.markets_quote(sym_id)['quotes'][0]
    cur_yield = (q.symbol(sym_id)['symbols'][0]['yield']) / 100
    cur_price = cur_price_data['lastTradePrice']
    if bod:
        cur_price = cur_price_data['openPrice']
    if (cur_price == 0) or bod is False:
        cur_price = cur_price_data['lastTradePrice']
    try:
        if (cur_price_data['bidPrice'] - cur_price_data['askPrice']) > (0.005 * cur_price):
            cur_price = (cur_price_data['bidPrice'] + cur_price_data['askPrice']) / 2
    except:
        cur_price = cur_price_data['lastTradePrice']
    return cur_price, cur_yield

def get_bod_pchg(q,ticker):
    sym_id = extract_symbolid(q, ticker)
    cur_price_data = q.markets_quote(sym_id)['quotes'][0]
    cur_price = cur_price_data['lastTradePrice']
    open_price = cur_price_data['openPrice']
    pchg =  cur_price/open_price - 1
    return pchg, cur_price


def opt_data(q, ticker, date_lim='all', bod=False):
    opt_df = extract_opt_data(q, ticker, date_lim)
    cur_price, cur_yield = get_price_yield(q, ticker, bod)
    expiry_list = list(opt_df['Expiry'].unique())
    master_df = pd.DataFrame()
    for i in expiry_list:
        store_df = opt_df[opt_df['Expiry'] == i]
        call_list = list(store_df['Call Code'])
        put_list = list(store_df['Put Code'])
        calls_df = pd.DataFrame(q.markets_options(optionIds=call_list)['optionQuotes'])
        puts_df = pd.DataFrame(q.markets_options(optionIds=put_list)['optionQuotes'])
        calls_df['CallPut'] = 'call'
        puts_df['CallPut'] = 'put'
        df = calls_df.append(puts_df)
        df['Expiry'] = i
        master_df = pd.concat([master_df, df])
    master_df['strike'] = master_df['symbol'].apply(lambda x: u.strike_finder(ticker, x))
    master_df['moneyness'] = master_df['strike'].apply(lambda x: float(x) / float(cur_price))
    master_df['Days to Expiry'] = master_df['Expiry'].apply(lambda x: u.bus_days(today, u.date_converter(x)))
    master_df = master_df[(master_df['Days to Expiry'] > 1)]
    if bod:
        master_df['Adj Days to Exp'] = master_df['Days to Expiry'].apply(lambda x: x-u.pct_day_passed())
        master_df['IV'] = master_df.apply(
            lambda x: iv.iv_solver(x['openPrice'], x['CallPut'], cur_price, x['strike'], 0.001, cur_yield,
                                   x['Adj Days to Exp']), axis=1)
    else:
        master_df['IV'] = master_df.apply(
            lambda x: iv.iv_solver(x['lastTradePrice'], x['CallPut'], cur_price, x['strike'], 0.001, cur_yield,
                                   x['Days to Expiry']), axis=1)
    master_df.dropna(subset=['IV'], inplace=True)
    master_df = master_df[master_df['IV'] > 1]
    master_df['adj_time'] = master_df['Days to Expiry'].apply(lambda x: x / 252)
    return master_df[cols]

## Make Watch List Snapper as this works

### To build previous vol surfaces:
### Access to past options: q.markets_candles(29949513, interval='OneDay',startTime='2020-04-15T09:30:00.583000-05:00')
### Gives us candlesticks (can use their close and open to price)
## Notes: adjust dates, need dates in the ISO format, look for a way to get rates dynamically for rf