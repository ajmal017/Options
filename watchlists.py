import utils as u
import itertools


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

my_port = ['HEXO.TO','AHPI','SHRM.CN','WELL.TO','OTEX.TO','DSG.TO','T.TO','MRT.UN.TO','CZR','HLF.TO','HR.UN.TO']

all_watchlist = [five_g, biotech, rona, disc, cad_tech, cad_lt, us_lt,misc_reits,mixed_reits,retail_reits,ind_reits, active_trade,
                 my_port]

opt_list = u.remove_duplicates(list(itertools.chain.from_iterable([biotech,rona,disc,active_trade])))
tot_list = u.remove_duplicates(list(itertools.chain.from_iterable(all_watchlist)))
