import os
import concurrent.futures
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
t = os.getenv("QKEY")

def get_vol_surface_omon(q, ticker, start_date = True,date_lim='all', rows=0, bod=False):
    opt_df = d.get_vol_surface(q, ticker, start_date,date_lim, bod)
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


def vol_comparison(ticker,start_date = True, rows=0, date_lim=4):
    surface_bod, bod_omon = get_vol_surface_omon(
        q, ticker, start_date,date_lim, rows, bod=True)
    surface_now, now_omon = get_vol_surface_omon(q, ticker,start_date, date_lim, rows)
    surface_dif = surface_now - surface_bod
    return surface_dif, now_omon, surface_now


def _surface_helper(ticker):
    try:
        surface_dif, now_omon, surface_now = vol_comparison(ticker, True,rows=10, date_lim=4)
        pct_chg, cur_price = d.get_bod_pchg(q, ticker)
        print('Vol Surface for %s' % ticker)
        print(surface_now)
        print('Vol Surface Changes for %s' % ticker)
        print(surface_dif)
        print('Price is currently {0}, changing {1} for {2}'.format("{:.2}".format(round(cur_price,2), "{:.2%}".format(pct_chg), ticker)))
        print('Volume monitor for %s' % ticker)
        print(now_omon)
    except Exception as e:
        print(ticker)


def print_surfaces(stock_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f = executor.map(_surface_helper,stock_list)
        for i in f:
            print(i)


if __name__=="__main__":
    t = '32co0bILJKn37TUGv9J2ARfhQv5-m5bt0'
    q = Questrade(grant_type=t, refresh_token=t)
    start = time.perf_counter()
    watchlist = w.opt_list
    print_surfaces(watchlist)
    end = time.perf_counter()
    print(f'Finish in {round(end-start,2)} seconds')
    # opt_monitor(60, w.xlb, date_lim=4)