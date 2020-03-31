import data as d
from questrade_api import Questrade
import itertools
import utils as u

five_g = ['INTC','QCOM','VZ','XLNX','NVDA','ADI','TMUS','MRVL','S','EXF.TO','AVGO','RCI.B.TO','FTG.TO']
cad_tech = ['QUIS.VN','CDAY.TO','SHOP.TO','REAL.TO','CSU.TO','TCS.TO','BRAG.VN']
biotech = ['APT','AHPI','CODX','INO','CBLI','BCYC','OPK','VIR','COCP','MRNA','SNY','GILD','BCRX','NVAX','LAKE','DVAX',
           'GSK','NNVC','VXRP']
rona = ['PRPL','TDOC','DPZ','WORK','ZM','CTXS','EBAY','NYT','TGT','ISRG','JNJ','CRWD','TEAM','RGR','CLX','SSTK','WMT',
        'ZG','CPB','OKTA','JD','PFE','KR','ALRM','ZNGA','ATVI','AMZN','GRUB','NFLX','SONO','PTON','MTCH','CENT','FB',
        'BABA','SIRI','TME','WIFI','YELP']
disc = ['RRR','UA','BYD','LULU','NKE','DIS','MAR','BA','HLT','DAL','AAL','LUV','ALK','CZR','NCLH','CCL','RCL','ERI']
cad_lt = ['VFF.TO','BIP.UN.TO','ACB.TO','DOL.TO','HMMJ.TO','WEED.TO','PZA.TO','RY.TO','AC.TO','ENB.TO','JWEL.TO',
          'ATD.B.TO','EDGE.TO','CYBR.TO','SU.TO','MFC.TO','ATZ.TO','T.TO','HLF.TO','HEXO.TO','FTS.TO','SLF.TO','TD.TO']
reits = ['DLR','SPG','WELL','BPY.UN.TO','NVU.UN.TO','MRT.UN.TO','IIP.UN.TO','REI.UN.TO','MI.UN.TO','SRU.UN.TO']
us_lt = ['DPZ','AMT','SQ','HD','MU','AMD','MA','F','JPM','A','GS','TTD','TGT','SBUX','JNJ','TWTR','BAC','NVDA','ETFC',
         'V','MCD','MSFT','ADBE','WMT','GM','AAPL','BRK.B','CVGW','SNAP','TU','FB','TSLA']

tot_list = u.remove_duplicates(list(itertools.chain.from_iterable([five_g,cad_tech,biotech,rona,disc,cad_lt,reits,us_lt])))

def monitor(watchlist=[], orders=False):
    t = input('Please enter api key:\n')
    q = Questrade(grant_type=t, refresh_token=t)
    if orders:
        my_orders = d.retrieve_orders(q)
        df = d.retrieve_symbolid_list(q, my_orders)
        df = df[['lastTradePrice', 'openPrice', 'limitPrice','pct_chg', 'abs_limit', 'pct_limit']]
        df = df.sort_values('pct_limit', ascending=True)
    elif watchlist == []:
        return 'Error'
    else:
        df = d.retrieve_symbolid_list(q, watchlist, True)
        df=df.sort_values('pct_chg', ascending=True)
    return df

print(monitor([],True))
# print(monitor(five_g))
# print(monitor(cad_tech))
# print(monitor(biotech))
# print(monitor(rona))
# print(monitor(disc))
# print(monitor(cad_lt))
# print(monitor(reits))
# print(monitor(us_lt))
# print(monitor(tot_list))