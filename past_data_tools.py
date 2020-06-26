import pandas as pd
import numpy as np

misc_storage_path = '/Users/djiang3/Desktop/Options Storage/Misc/'
comp_list = ['underlying', 'bidPrice', 'askPrice', 'lastTradePrice', 'openInterest', 'volume', 'CallPut', 'Expiry',
             'strike', 'moneyness', 'Days to Expiry', 'Adj Price', 'volatility', 'delta', 'gamma', 'theta', 'vega',
             'rho']
total_oi_list = ['underlying','lastTradePrice','openInterest','volume','CallPut','Expiry','strike']
oi_chg_list = ['underlying','lastTradePrice','openInterest','openInterest_chg','volume','CallPut','Expiry','strike']


class Historical_Opt_Analysis:
    def __init__(self, start_date, end_date, total_thresh, chg_thresh, ticker_list='default'):
        self.start = start_date
        self.end = end_date
        self.total_thresh = total_thresh
        self.chg_thresh = chg_thresh
        self.start_df = Historical_Opt_Analysis.get_hist_data(self, start_date)
        self.end_df = Historical_Opt_Analysis.get_hist_data(self, end_date)
        if ticker_list == 'default':
            self.ticker_list = set(
                set(list(self.start_df['underlying'].unique())) & set(list(self.end_df['underlying'].unique())))
        else:
            self.ticker_list = ticker_list

    '''Get df from existing file for a given date
    function(date) -> df of historical options data of the date
    '''

    def get_hist_data(self, date):
        file_name = 'Daily Snap ' + date + '.csv'
        path = misc_storage_path + file_name
        df = pd.read_csv(path).set_index('symbol')
        return df[comp_list]

    ''' Get OTM weird activities
    function(df, alist_of_stocks) -> df of strange OTM OI activities
    '''

    def otm_activities(self, ticker):
        df_start = self.end_df
        df_end = self.start_df
        df_start = df_start[df_start['underlying'] == ticker].replace(to_replace='None', value=np.nan).fillna(0)
        df_end = df_end[df_end['underlying'] == ticker].replace(to_replace='None', value=np.nan).fillna(0)
        expiry_list = set(set(list(df_start['Expiry'].unique())) & set(list(df_end['Expiry'].unique())))
        output_oi_chg = pd.DataFrame()
        deep_otm_oi = pd.DataFrame()
        for i in expiry_list:
            df_start_store = df_start[df_start['Expiry'] == i]
            df_end_store = df_end[df_end['Expiry'] == i]
            oi_sum = df_start_store['openInterest'].sum()
            oi_count = df_start_store['openInterest'].count()
            df_start_store = df_start_store[(df_start_store['moneyness'] < 0.85) | (df_start_store['moneyness'] > 1.15)]
            df_end_store = df_end_store[(df_end_store['moneyness'] < 0.85) | (df_end_store['moneyness'] > 1.15)]
            avg_atm_start = oi_sum / (oi_count - df_start_store['openInterest'].count())
            oi_chg = (df_start_store['openInterest'].to_frame() - df_end_store['openInterest'].to_frame()).dropna()
            total_oi = df_start_store[abs(df_start_store['openInterest']) > self.total_thresh * avg_atm_start]
            oi_chg = oi_chg[abs(oi_chg['openInterest']) > self.chg_thresh * avg_atm_start].merge(df_start_store,
                                                                                                 how='inner',
                                                                                                 left_index=True,
                                                                                                 right_index=True)
            oi_chg.rename(columns={"openInterest_x": "openInterest_chg","openInterest_y":"openInterest"}, inplace=True)
            output_oi_chg = output_oi_chg.append(oi_chg).drop_duplicates(keep='first')[oi_chg_list]
            deep_otm_oi = deep_otm_oi.append(total_oi).drop_duplicates(keep='first')[total_oi_list]
        return output_oi_chg, deep_otm_oi


test = Historical_Opt_Analysis('2020-06-24', '2020-06-23', 1.5, 2)
print(test.otm_activities('AAPL'))

''' Get ATM or closer to the money big movements in IV
function(df, alist_of_stocks -> df of strange ATM vol/Greek activities
'''

'''  
Vol backfiller
'''

'''Need to create a df that would have the price of vols at a date for a list of stocks'''

'''To Do List:
Find a way to compare vols
Make PAVS
'''
