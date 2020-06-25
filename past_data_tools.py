import pandas as pd

misc_storage_path = '/Users/djiang3/Desktop/Options Storage/Misc/'
comp_list = ['underlying','bidPrice','askPrice','lastTradePrice','openInterest','volume','CallPut','Expiry','strike','moneyness','Days to Expiry','Adj Price','volatility','delta','gamma','theta','vega','rho']

'''Get df from existing file for a given date
function(date) -> df of historical options data of the date
'''
def get_hist_data(date):
    file_name = 'Daily Snap ' + date + '.csv'
    path = misc_storage_path + file_name
    df = pd.read_csv(path).set_index('symbol')
    return df[comp_list]

print(get_hist_data('2020-06-22'))




''' Get OTM weird activities
function(df, alist_of_stocks) -> df of strange OTM OI activities
'''

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