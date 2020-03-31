import datetime
import numpy as np
import pandas as pd
import itertools

today = datetime.datetime.today().date()
skew_storage_path = '/Users/djiang3/Desktop/Options Storage/Vol Skew Storage/'
misc_storage_path = '/Users/djiang3/Desktop/Options Storage/Misc/'


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
    date = datetime.datetime.today().strftime('%Y-%m-%d-%H')
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


def inc_creator(top, bottom, increment):
    alist = []
    i = bottom
    while i <= top + 0.1:
        alist.append(round(i, 1))
        i += increment
    df = pd.DataFrame(alist, columns=['Moneyness'])
    return df, alist


def nearest_strikes(k, alist, num):
    above_list = [x >= k for x in alist]
    below_list = [x < k for x in alist]
    ab_function = lambda list_value: abs(list_value - k)
    final_ab, final_bl = []
    ab_tot, below_tot = num
    ## So Far this assumes that we have num strikes closest, might not be the case
    for i in range(num):
        if above_list is not []:
            c_above = min(above_list, key=ab_function)
            final_ab.append(c_above)
            above_list.remove(c_above)
            ab_tot -= 1
    below_tot += ab_tot
    if below_list is not []:
        c_below = min(below_list, key=ab_function)
        final_bl.append(c_below)
        below_list.remove(c_below)

def moneyness_adj(top, bottom, increment, opt_df):
    opt_df = opt_df[['strike', 'Expiry', 'CallPut', 'openInterest', 'moneyness', 'IV']]
    mdf, mlist = inc_creator(top, bottom, increment)

def remove_duplicates(alist):
    res = []
    [res.append(x) for x in list(alist) if x not in res]
    return res

# print(inc_creator(1.2, 0.8, 0.1))
# trial = pd.read_csv(r'/Users/djiang3/Desktop/Options Storage/Misc/FBBOD 2020-03-30-19.csv')
# trial = trial[['strike','Expiry','CallPut','openInterest','moneyness','IV']]
