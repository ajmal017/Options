import os
from datetime import datetime
import time
import data as d
import utils as u
from questrade_api import Questrade
import pandas as pd
import watchlists as w

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

cols = ['symbol', 'lastTradePrice', 'volume', 'openInterest',
        'CallPut', 'Expiry', 'strike', 'moneyness']


def get_vol_surface_omon(q, ticker, date_lim='all', rows=0, bod=False):
    opt_df = d.opt_data(q, ticker, date_lim, bod)
    omon_df = omon(opt_df, rows, sort_by='volume')
    vol_surface = u.vol_surface_data(1.2, 0.8, 0.05, opt_df)
    return vol_surface, omon_df


'''Can change what we sort by; eventually this should be change in OI; need to snap a different set of data and
perhaps the moneyness constraint could get taken out/optionalized'''


def omon(opt_df, rows=0, sort_by='volume'):
    opt_df = opt_df[cols]
    opt_df = opt_df[(opt_df['moneyness'] <= 0.975) |
                    (opt_df['moneyness'] >= 1.025)]
    opt_df = opt_df.sort_values(sort_by, ascending=False)
    if rows != 0:
        opt_df = opt_df.head(rows)
    return opt_df


'''For this, we are just trying to get the 4 closest vol tenors'''


def vol_comparison(q, ticker, rows=0, date_lim=4):
    surface_bod, bod_omon = get_vol_surface_omon(
        q, ticker, date_lim, rows, bod=True)
    surface_now, now_omon = get_vol_surface_omon(q, ticker, date_lim, rows)
    surface_dif = surface_now - surface_bod
    return surface_dif, now_omon


''' Only pass in one list of tickers; computationally much more expensive'''


def execute(q, freq, watchlist, rows, date_lim=4):
    if isinstance(watchlist, list):
        for i in watchlist:
            print("Current ticker is %s" % i)
            try:
                surface_dif, now_omon = vol_comparison(q, i, rows, date_lim)
                pct_chg = d.get_bod_pchg(q, i)
                print('Near Term Vol Surface Chg for %s' % i)
                print(surface_dif)
                print('Price change for %s' % i)
                print(pct_chg)
                print('Volume monitor for %s' % i)
                print(now_omon)
            except:
                print('Error for ticker is %s' % i)
    else:
        surface_dif, now_omon = vol_comparison(q, watchlist, date_lim)
        pct_chg = d.get_bod_pchg(q, watchlist)
        print('Vol Surface for %s' % watchlist)
        print(surface_dif)
        print('Price change for %s' % watchlist)
        print(pct_chg)
        print('Volume monitor for %s' % watchlist)
        print(now_omon)
    time.sleep(freq)


# print(vol_comparison('FB', 3))
'''Note, for the OMON function, we have to set up a recording method before we can look at chg in OI; can look at OI
and volume for now for each strike (ie. most traded; perhaps look into most traded thats not ATM'''

t = os.getenv("QUESTRADE_KEY")


def opt_monitor(freq, watchlist, rows=0, date_lim=0):
    q = Questrade(grant_type=t, refresh_token=t)
    seconds = freq*60
    print("Snapping vol data every %s minutes" % freq)
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print("Current time is %s" % (now))
        execute(q, seconds, watchlist, rows, date_lim)


opt_monitor(5, w.biotech, date_lim=4)
