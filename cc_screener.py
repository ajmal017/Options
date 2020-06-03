import pandas as pd
import data as d

cols = ['underlying','symbol','strike','Expiry','CallPut','openInterest','bidPrice','askPrice','lastTradePrice']

# sym_id = d.extract_symbolid(q, ticker)
# ohlc_df = d.retrieve_past_price(q, ticker, '2020-04-14', False, '2020-05-14')
# ohlc_df['start'] = ohlc_df['start'].apply(lambda x: x[:10])

def covered_call_screener(q,ticker,date_lim):
    master_df = d.get_opt_df(q, ticker, True, date_lim, False)
    master_df = master_df[[cols]]
    cur_price, cur_yield = d.get_price_yield(q, ticker, True)
    expiry_list = list(master_df['Expiry'].unique())
