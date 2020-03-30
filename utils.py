import datetime
import numpy as np

today = datetime.datetime.today().date()
skew_storage_path = '/Users/djiang3/Desktop/Options Storage/Vol Skew Storage/'
misc_storage_path = '/Users/djiang3/Desktop/Options Storage/Misc/'

def date_converter(date_str):
    dt_obj = datetime.datetime.strptime(date_str,'%Y-%m-%d')
    return dt_obj.date()

def bus_days(start,end):
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

def strike_finder(ticker,s):
    tick_len = len(ticker)
    for i in range(6,10):
        if is_number(s[i+tick_len:]):
            return float(s[i+tick_len:])
    else:
        return 0

