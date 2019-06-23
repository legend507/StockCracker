'''
2018-07-22, download stock data from Yahoo Finance

This script does the following errands:
1. automatically download stock market data (.csv), and save the data under ./data/stock/*
2. automatically download FX data, 
3. automatically download BitCoin data, 
'''
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf              # need to install this with pip, refer to https://pypi.org/project/fix-yahoo-finance/
import datetime as dt
import os

#--------------- Stock Data -------------------------
# target stock names, and save path
class Tickers:
    def __init__(self):
        self.tickers = {
                #--- Index
                '^N225':     './data/stock/nikkei/',             # Nikkei 225 Index
                #--- Vehicle OEMs
                '7261.T':    './data/stock/mazda/',              # Mazda, Nikkei
                '7203.T':    './data/stock/toyota/',             # Toyota, Nikkei
                '7201.T':    './data/stock/nissan/',             # Nissan, Nikkei
                '7267.T':    './data/stock/honda/',              # Honda, Nikkei
                #--- Entertainmen
                '4680.T':    './data/stock/round1/',             # Round 1, Nikkei
                '2412.T':    './data/stock/benefitone/',         # BenefitOne, Nikkei
                '7494.T':    './data/stock/nintendo/',           # Nintendo, game company, Nikkei
                #--- Consumer Electronics Maker
                '6752.T':    './data/stock/panasonic/',          # Panasonic, Nikkei
                '6758.T':    './data/stock/sony/',               # Sony, Nikkei
                '3993.T':    './data/stock/pksha/',              # PKSHA, Toyota owned AI software company, Nikkei
                '6501.T':    './data/stock/hitachi/',            # Hitachi, Nikkei
                '7731.T':    './data/stock/nikon/',              # Nikon camera maker, Nikkei
                '7751.T':    './data/stock/canon/',              # Canon camera maker, Nikkei
                '6902.T':    './data/stock/denso/',              # Denso, Toyota's bitch, Nikkei
                '6503.T':    './data/stock/mitsubishi-electric/',# Mitsubishi-electric, 
                '6502.T':    './data/stock/toshiba/',            # Toshiba, seems they are coming back    
                #--- Tech
                '9984.T':    './data/stock/softbank/',           # Softbank, 
                '9613.T':    './data/stock/nttdata/',            # NTT Data
                '9432.T':    './data/stock/ntt/',                # NTT
                '3807.T':    './data/stock/fisco/',              # Fisco, making investing tools, Nikkei
                '4716.T':    './data/stock/oracle/',             # Oracle Japan, Nikkei
                '4755.T':    './data/stock/rakuten/',            # Rakuten, 
                '9433.T':    './data/stock/kddi/',               # KDDI, 
                '3966.T':    './data/stock/uzabase/',            # UZABASE, news/fiance analyzor
                '6146.T':    './data/stock/disco/',              # Disco, material/device maker
                '3655.T':    './data/stock/brainpad/',           # BrainPad, some big data company
                '4385.T':    './data/stock/mercari/',            # Mercari, a mobile app eCommerce company
                '3092.T':    './data/stock/zozo/',               # ZOZO, eCommerce company
                #--- Banking
                '8411.T':    './data/stock/mizuho/',             # Mizuho Finance Group, Nikkei
                '8306.T':    './data/stock/mitsubishi-ufj/',     # Mitsubishi UFJ
                '8316.T':    './data/stock/smfg/',               # 住友 Finance Group
                #--- Food & Drinks
                '2579.T':    './data/stock/coca-cola/',          # Coca Cola Japan Holdings, 
                '2587.T':    './data/stock/suntory/',            # Suntory
                '2502.T':    './data/stock/asahi/',              # Asahi
                #--- Service
                '6098.T':    './data/stock/recruit/',            # Recruit
                '6178.T':    './data/stock/jppost/',             # 日本郵政
                '9603.T':    './data/stock/his/',                # H.I.S
                #--- Retail
                '8267.T':    './data/stock/aeon/',               # AEON, supermarket,
                #--- Transportation
                '9202.T':    './data/stock/ana/',                # ANA airline
                '9201.T':    './data/stock/jal/',                # JAL airline
                '9020.T':    './data/stock/jr-east/',            # East Japan Railway
                '9021.T':    './data/stock/jr-west/',            # West Japan Railway
                #--- Chemistry
                '4911.T':    './data/stock/shiseido/',           # 資生堂
                '4901.T':    './data/stock/fujifilm/',           # Fuji Film
                '3402.T':    './data/stock/toray/',              # 東レ
                #--- Trading 
                '8001.T':    './data/stock/idochu/',             # 伊藤忠商事
                #--- Insurance
                '8766.T':    './data/stock/tokiomarine/',        # 東京海上日動
                #--- Oil
                '5020.T':    './data/stock/jxtg/',               # JXTG, 
                #--- TV
                '9413.T':    './data/stock/tv-tokyo/',           # TV Tokyo
                '9409.T':    './data/stock/tv-asahi/',           # TV Asahi
                #--- Media
                '2371.T':    './data/stock/kakaku/',             # Kakaku.com

                }


if __name__ == '__main__':
    t = Tickers()

    # set start, end date, begin download data
    yf.pdr_override()
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.today()

    print('Downloading: Stock data')
    for key, value in t.tickers.items():
        try:
            print('Getting: ' + key + ' | ' + value[13:-1])
            data = pdr.get_data_yahoo(key, start=start, end=end)
            #print(data)
        except:
            print('Failed to download data')
            os.system('pause')
            exit(1)

        os.makedirs(value, exist_ok=True)
        data.to_csv(value + 'data.csv', encoding='utf-8')

    #--------------- FX Data -------------------------
    import httplib2
    import sys
    import pandas_datareader as web
    from datetime import datetime

    print('Downloading: FX data')


    content = web.DataReader(
        'DEXJPUS', 
        'fred', 
        start=datetime(2000, 1, 1), 
        end=datetime.today())
    print(content.tail())

    path = './data/FX/USDJPY/'
    os.makedirs(path, exist_ok=True)
    content.to_csv(path + 'data.csv')

    print('Downloading: BitCoin data')
    #--------------- BitCoin Data -------------------------
    from BTCUpdate import updateCryptoCurrencyData
    updateCryptoCurrencyData()