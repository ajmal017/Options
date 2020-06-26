import concurrent.futures
import data as d
from questrade_api import Questrade
import pandas as pd
import watchlists as w
import utils as u
import time


def _helper(x):
    try:
        df = d.get_opt_df(q, x)
        return df
    except Exception as e:
        pass

def scrape_data(stock_list):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f = executor.map(_helper,stock_list)
        master_df = pd.DataFrame()
        for i in f:
            master_df = master_df.append(i)
    return master_df

'''Change t into the new api code and click the play button (or run this)'''
if __name__=="__main__":
    t = 'QnyWpNVssyMzDo-S2f54nUoLGDuMAeiJ0'
    q = Questrade(grant_type=t, refresh_token=t)
    start = time.perf_counter()
    df = scrape_data(w.track_list)
    u.snap_vols(df,'Daily Snap')
    end = time.perf_counter()
    print(f'Finish in {round(end-start,2)} seconds')



