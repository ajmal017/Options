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

def extract_symbolid(q, ticker):
    access_dict = q.symbols_search(prefix=ticker)['symbols']
    total_len = len(access_dict) - 1
    symbol_id = []
    for i in range(total_len):
        if (access_dict[i]['isTradable'] == True) and (access_dict[i]['isQuotable'] == True):
            if access_dict[i]['symbol'] == ticker:
                symbol_id.append((ticker, access_dict[i]['symbolId']))
    if len(symbol_id) == 1:
        return symbol_id[0][1]
    else:
        return symbol_id


'''Returns a dataframe with each ticker's option codes for each expiry'''

def extract_opt_chain(q, ticker, date_lim='all',bod=False):
    symbol_id = extract_symbolid(q, ticker)
    cur_price, cur_yield = get_price_yield(q, ticker,bod)
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
    df.columns = ['Strike','Call Code','Put Code','Expiry','Moneyness']
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


def opt_data(q, ticker, date_lim='all', bod=False):
    opt_df = extract_opt_chain(q, ticker, date_lim)
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
    master_df['strike'] = master_df['symbol'].apply(lambda x: u.strike_finder(ticker,x))
    master_df['moneyness'] = master_df['strike'].apply(lambda x: float(x) / float(cur_price))
    master_df['Days to Expiry'] = master_df['Expiry'].apply(lambda x: u.bus_days(today, u.date_converter(x)) - 1)
    master_df = master_df[(master_df['Days to Expiry'] > 0)]
    if bod:
        master_df['Days to Expiry BOD'] = master_df['Days to Expiry'].apply(lambda x: x+1)
        master_df['IV'] = master_df.apply(
            lambda x: iv.iv_solver(x['openPrice'], x['CallPut'], cur_price, x['strike'], 0.01, cur_yield,
                                   x['Days to Expiry BOD']), axis=1)
    else:
        master_df['IV'] = master_df.apply(
            lambda x: iv.iv_solver(x['lastTradePrice'], x['CallPut'], cur_price, x['strike'], 0.01, cur_yield,
                                   x['Days to Expiry']), axis=1)
    master_df.dropna(subset=['IV'], inplace=True)
    master_df = master_df[master_df['IV'] > 1]
    master_df['adj_time'] = master_df['Days to Expiry'].apply(lambda x: x / 252)
    return master_df[cols]

def retrieve_positions(q):
    acc_num = q.accounts['accounts'][0]['number']
    positions = q.account_positions(acc_num)['positions']
    position_df = pd.DataFrame(positions)
    return position_df['symbolId']

def retrieve_orders(q):
    acc_num = q.accounts['accounts'][0]['number']
    positions = q.account_orders(acc_num)['orders']
    position_df = pd.DataFrame(positions)
    return position_df['symbolId']

