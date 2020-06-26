import datetime
import numpy as np
import pandas as pd
import itertools
from datetime import timedelta

today = datetime.datetime.today().date()
skew_storage_path = '/Users/djiang3/Desktop/Options Storage/Vol Skew Storage/'
misc_storage_path = '/Users/djiang3/Desktop/Options Storage/Misc/'

def chg_date(date_str,num_days):
    datetime_fmt = date_converter(date_str)
    new_date = datetime_fmt + timedelta(days=num_days)
    str_date = new_date.strftime('%Y-%m-%d')
    return str_date


def date_converter(date_str):
    dt_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    return dt_obj.date()


def bus_days(start, end):
    days = np.busday_count(start, end)
    return days


'''Name must be some type of string
name = 'Vol Skews' goes to Vol Skew Storage
Anything else goes to Misc'''


def snap_vols(table_to_excel, name):
    if name == 'Vol Skews':
        path = skew_storage_path
    else:
        path = misc_storage_path
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    file_name = name + ' ' + date + '.csv'
    table_to_excel.to_csv(path + file_name)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def strike_finder(ticker, s):
    tick_len = len(ticker)
    for i in range(6, 10):
        if is_number(s[i + tick_len:]):
            return float(s[i + tick_len:])
    else:
        return 0


def remove_duplicates(alist):
    res = []
    [res.append(x) for x in list(alist) if x not in res]
    return res


def pct_day_passed(start_hour = 9, start_minute = 30):
    now = datetime.datetime.now()
    cur_hour = now.hour
    cur_minute = now.minute
    total_min_dif = (cur_hour - start_hour)*60 +(cur_minute - start_minute)
    pct_day = total_min_dif/390
    return pct_day

'''All used in vol surface smoothing and calculations'''


def inc_creator(top, bottom, inc):
    alist = []
    i = bottom
    while i <= top + inc:
        alist.append(round(i, 2))
        i += inc
    df = pd.DataFrame(alist, columns=['Moneyness'])
    return df


def nearest_moneyness(m, alist, num_opt, inc):
    above_list = sorted(list(filter(lambda x: x > m, alist)))
    below_list = sorted(list(filter(lambda x: x <= m, alist)))
    if len(above_list) > num_opt:
        above_list = above_list[:num_opt]
    if len(below_list) > num_opt:
        below_list = below_list[num_opt:]
    final_list = sorted(above_list + below_list)
    final_list = list(filter(lambda x: (x <= m + inc or x <= m - inc), final_list))
    return final_list


'''atype can be call, put, but by default it is all and this takes the weighted average of moneyness's IV and creates
a dataframe of moneyness, strike, and IV'''


def moneyness_comb(df, atype='all'):
    if atype != 'all':
        df = df[df['CallPut'] == atype]
    expiry_list = list(df['Expiry'].unique())
    master_df = pd.DataFrame()
    for i in expiry_list:
        temp_df = df[df['Expiry'] == i]
        call_df = temp_df[temp_df['CallPut'] == 'call'].set_index('moneyness')[['strike', 'IV', 'openInterest']]
        put_df = temp_df[temp_df['CallPut'] == 'put'].set_index('moneyness')[['strike', 'IV', 'openInterest']]
        call_df.rename(columns={'strike': 'Call Strike', 'IV': 'Call IV', 'openInterest': 'Call OI'}, inplace=True)
        put_df.rename(columns={'strike': 'Put Strike', 'IV': 'Put IV', 'openInterest': 'Put OI'}, inplace=True)
        new_df = call_df.merge(put_df, how='outer', left_index=True, right_index=True).fillna(0)
        new_df[['Call OI', 'Put OI']] = new_df[['Call OI', 'Put OI']].astype(int)
        new_df[['Call IV', 'Put IV']] = new_df[['Call IV', 'Put IV']].astype(float)
        new_df['Total OI'] = new_df['Call OI'] + new_df['Put OI']
        new_df['IV'] = new_df['Call IV'] * (new_df['Call OI'] / new_df['Total OI']) + new_df['Put IV'] * (
                new_df['Put OI'] / new_df['Total OI'])
        df_store = new_df
        df_store['Expiry'] = i
        master_df = pd.concat([master_df, df_store])
    cols = ['Call Strike', 'Put Strike', 'Total OI', 'IV', 'Expiry']
    master_df = master_df[cols]
    master_df.dropna(inplace=True)
    return master_df


def iv_moneyness_solve(money_df, m_list):
    if len(m_list) == 0:
        return 0
    else:
        filter_df = money_df[money_df.index.isin(m_list)]
        iv_mean = filter_df['IV'].mean()
        filter_df = filter_df[(filter_df['IV'] < 1.2 * iv_mean) | (filter_df['IV'] > 0.8 * iv_mean)]
        if len(filter_df) == 0:
            return 0
        else:
            total_oi = filter_df['Total OI'].sum()
            filter_df['weights'] = filter_df['Total OI'] / total_oi
            filter_df['weighted avg'] = filter_df['weights'] * filter_df['IV']
            iv_weighted = filter_df['weighted avg'].sum()
    return iv_weighted


# trial = pd.read_csv(r'/Users/djiang3/Desktop/Options Storage/Misc/Moneyness Builder 2020-04-05-19.csv')

def moneyness_chart_fill(m_range, opt_df):
    alist = list(opt_df.index.values)
    expiry = list(opt_df['Expiry'])[0]
    m_range[expiry] = np.nan
    for m in list(m_range.index.values):
        moneyness_list = nearest_moneyness(m, alist, 2, 0.025)
        iv = iv_moneyness_solve(opt_df, moneyness_list)
        m_range.loc[m] = iv
    return m_range


def vol_surface_data(top, bottom, inc, opt_df):
    opt_df = moneyness_comb(opt_df, atype='all')
    expiry_list = list(opt_df['Expiry'].unique())
    master_df = inc_creator(top, bottom, inc).set_index('Moneyness')
    for i in expiry_list:
        temp_df = opt_df[opt_df['Expiry'] == i]
        m_range = inc_creator(top, bottom, inc).set_index('Moneyness')
        store_df = moneyness_chart_fill(m_range, temp_df)
        master_df = master_df.merge(store_df, how='inner', left_index=True, right_index=True)
    return master_df

def stale_price_proxy(bid,ask,volume,last):
    if volume <= 20:
        return float((bid+ask)/2)
    else:
        return float(last)
