import utils as u
import itertools
import pandas as pd

ticker_file = pd.read_csv(r'/Users/djiang3/Desktop/Options Storage/Tickers.csv')

nasdaq = ticker_file['NASDAQ Ticker'].dropna().to_list()
sptsx = ticker_file['SPTSX60 Ticker'].dropna().to_list()
sp = ticker_file['S&P Ticker'].dropna().to_list()

track_list = list(itertools.chain.from_iterable([nasdaq,sptsx,sp]))

five_g = ['INTC', 'QCOM', 'VZ', 'XLNX', 'NVDA', 'ADI', 'TMUS', 'MRVL', 'EXF.TO', 'AVGO', 'RCI.B.TO', 'FTG.TO']
cad_tech = ['QUIS.VN', 'CDAY.TO', 'SHOP.TO', 'REAL.TO', 'CSU.TO', 'TCS.TO', 'BRAG.VN']
biotech = ['APT', 'AHPI', 'CODX', 'INO', 'CBLI', 'BCYC', 'OPK', 'VIR', 'COCP', 'MRNA', 'SNY', 'GILD', 'BCRX', 'NVAX',
           'LAKE', 'DVAX',
           'GSK', 'NNVC', 'VXRP']
rona = ['PRPL', 'TDOC', 'DPZ', 'WORK', 'ZM', 'CTXS', 'EBAY', 'NYT', 'TGT', 'ISRG', 'JNJ', 'CRWD', 'TEAM', 'RGR', 'CLX',
        'SSTK', 'WMT',
        'ZG', 'CPB', 'OKTA', 'JD', 'PFE', 'KR', 'ALRM', 'ZNGA', 'ATVI', 'AMZN', 'GRUB', 'NFLX', 'SONO', 'PTON', 'MTCH',
        'CENT', 'FB',
        'BABA', 'SIRI', 'TME', 'WIFI', 'YELP']
disc = ['RRR', 'UA', 'BYD', 'LULU', 'NKE', 'DIS', 'MAR', 'BA', 'HLT', 'DAL', 'AAL', 'LUV', 'ALK', 'CZR', 'NCLH', 'CCL',
        'RCL', 'ERI']
cad_lt = ['VFF.TO', 'BIP.UN.TO', 'ACB.TO', 'DOL.TO', 'HMMJ.TO', 'WEED.TO', 'PZA.TO', 'RY.TO', 'AC.TO', 'ENB.TO',
          'JWEL.TO',
          'ATD.B.TO', 'EDGE.TO', 'CYBR.TO', 'SU.TO', 'MFC.TO', 'ATZ.TO', 'T.TO', 'HLF.TO', 'HEXO.TO', 'FTS.TO',
          'SLF.TO', 'TD.TO']
misc_reits = ['DLR', 'SPG', 'WELL', 'NVU.UN.TO', 'IIP.UN.TO', 'MI.UN.TO', 'CSH.UN.TO','AP.UN.TO','D.UN.TO']
mixed_reits=['CUF.UN.TO','REF.UN.TO','CRR.UN.TO','GRT.UN.TO','HR.UN.TO','MRT.UN.TO','PRV.UN.TO','TNT.UN.TO','BPY.UN.TO']
retail_reits = ['CRT.UN.TO','REI.UN.TO','SRT.UN.TO','PLZ.UN.TO','SRU.UN.TO']
ind_reits = ['NXR.UN.VN','DIR.UN.TO','SMU.UN.TO','WIR.UN.TO']
us_lt = ['DPZ', 'AMT', 'SQ', 'HD', 'MU', 'AMD', 'MA', 'F', 'JPM', 'A', 'GS', 'TTD', 'TGT', 'SBUX', 'JNJ', 'TWTR', 'BAC',
         'NVDA', 'ETFC',
         'V', 'MCD', 'MSFT', 'ADBE', 'WMT', 'GM', 'AAPL', 'BRK.B', 'CVGW', 'SNAP', 'TU', 'FB', 'TSLA']
active_trade = ['TWTR','NET','FB','SNAP','GOOG','INTC','BPY.UN.TO','WELL','MSFT','SQ','AAPL','AKAM','WIX','TSLA','ETSY','NFLX','WMT','TDOC','ZM','SHOP.TO']

all_watchlist = [five_g, biotech, rona, disc, cad_tech, cad_lt, us_lt,misc_reits,mixed_reits,retail_reits,ind_reits, active_trade,
                 my_port]

# opt_list = ['AMD','AKAM','CCL','DHT','CZR','RCL','BA','RRR','BPY','ALK','DIS','NVAX','TDOC','ZM','WIX','WORK','MSFT','XLE','FB']
# opt_list = ['XLE','XLB','XLI','XLY','XLP','XLV','XLF','SMH','XTL','XLU','IYR','CCL','DHT','CZR','RCL','BA','TDOC','ZM']
opt_list = ['RPD','PFPT','TTD','TRIP','DBX','AGN','ROKU','NET','GPRO','MCHP','QRVO','YELP','ZG']
'''Sector Lists for a deeper look'''
xle=['CVX','XOM','PSX','COP','COP','EOG','VLO','KMI','MPC','PXD','OXY','HAL','SLB']
xlb = ['LIN','NEM','APD','ECL','SHW','DD','DOW','PPG','BLL','CTVA','FCX','IP']
xli = ['UNP','HON','RTX','LMT','MMM','BA','UPS','CAT','GE','CSX','DE','NOC']
xly=['AMZN','HD','MCD','NKE','SBUX','LOW','TJX','TGT','EBAY','YUM','MAR','CMG','MGM','CCL']
xlp = ['PG','PEP','KO','WMT','MO','PM','COST','CL','GIS','STZ','CLX','KMB']
xlv = ['JNJ','UNH','PFE','MRK','ABT','BMY','TMO','AMGN','CI','ANTM','GILD','CVS']
xlf = ['BRK.B','JPM','BAC','WFC','C','GS','SPGI','CME','NLK','ICE','AXP']
smh=['TSM','INTC','NVDA','ASML','AVGO','TXN','AMD','QCOM','XLNX','SWKS','MU']
xtl=['BAND','VG','TMUS','ANET','CIEN','LITE','CCOI','FFIV','CSCO','JNPR','UI']
xlu= ['NEE','D','DUK','SO','AEP','EXC','SRE','WEC','ED','ES','PEG','FE','AWK']
iyr = ['AMT','PLD','CCI','AQIX','DLR','PSA','WELL','SPG','O','PSA','BXP','CBRE']

tot_list = u.remove_duplicates(list(itertools.chain.from_iterable(all_watchlist)))