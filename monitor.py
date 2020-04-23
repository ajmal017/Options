import os
import time
import data as d
from questrade_api import Questrade
import watchlists as w
import pandas as pd
from datetime import datetime
import vol as v

pd.set_option('display.max_rows', 500)

t = os.getenv("QKEY")

# noinspection PySimplifyBooleanCheck


def monitor(q, watchlist=[], orders=False):
    if orders:
        my_orders = d.retrieve_orders(q)
        df = d.retrieve_symbolid_list(q, my_orders)
        df = df[['lastTradePrice', 'openPrice', 'limitPrice',
                 'pct_chg', 'abs_limit', 'pct_limit']]
        df = df.sort_values('pct_limit', ascending=True)
    elif watchlist == []:
        return 'Error'
    else:
        df = d.retrieve_symbolid_list(q, watchlist, True)
        df = df.sort_values('pct_chg', ascending=True)
    return df


def execute(q, freq, watchlist, orders):
    print('Order Monitor')
    try:
        print(monitor([], True))
    except:
        print('Current Orders Error')
    if any(isinstance(el, list) for el in watchlist):
        for i in watchlist:
            print("Current watchlist is %s" % i)
            try:
                print(monitor(q, i, orders))
            except:
                print('Error for watchlist')
    else:
        print(monitor(q, watchlist, orders))
    time.sleep(freq)


def repeat_monitor(freq, watchlist, orders=False):
    q = Questrade(grant_type=t, refresh_token=t)
    seconds = freq * 60
    print("Snapping data every %s minutes" % (freq))
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print("Current time is %s" % (now))
        execute(q, seconds, watchlist, orders)


def pilot_monitor(pos_freq, pos_watchlist, opt_freq, opt_watchlist, rows=10, date_lim=4, orders=False):
    q = Questrade(grant_type=t, refresh_token=t)
    pos_seconds = pos_freq * 60
    opt_seconds = opt_freq * 60
    print("Snapping positions data every %s minutes and options data every %s minutes" % (pos_freq, opt_freq))
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print("Current time is %s" % (now))
        execute(q, pos_seconds, pos_watchlist, orders)
        if now.hour == 15:
            v.execute(q, opt_seconds, opt_watchlist, rows, date_lim)


# pilot_monitor(5,w.all_watchlist,10,w.opt_list)
if __name__=="__main__":
    repeat_monitor(5, w.all_watchlist)

# Checks orders
# print(monitor([],True))

# Gives snap of a watchlist watchlist
# print(monitor(w.five_g))
