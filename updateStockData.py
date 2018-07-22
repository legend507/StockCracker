'''
2018-07-22, download stock data from Yahoo Finance

This script does the following errands:
1. automatically download stock market data (.csv), and save the data under ./data/stock/*
(ToDo) 2. automatically download FX data, 
(ToDo) 3. automatically download BitCoin data, 
'''

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf              # need to install this with pip, refer to https://pypi.org/project/fix-yahoo-finance/
import datetime as dt
import os

#--------------- Stock Data -------------------------
# target stock names, and save path
tickets = {
           #--- Index
           '^N225':     './data/stock/nikkei/',             # Nikkei 225 Index
           #--- Vehicle OEMs
           '7261.T':    './data/stock/mazda/',              # Mazda, Nikkei
           '7203.T':    './data/stock/toyota/',             # Toyota, Nikkei
           '7201.T':    './data/stock/nissan/',             # Nissan, Nikkei
           '7267.T':    './data/stock/honda/',              # Honda, Nikkei
           #--- Entertainmen
           '4680.T':    './data/stock/round1/',             # Round 1, Nikkei
           #--- Consumer Electronics Maker
           '6752.T':    './data/stock/panasonic/',          # Panasonic, Nikkei
           }

# set start, end date, begin download data
yf.pdr_override()
start = dt.datetime(2000, 1, 1)
end = dt.datetime.today()

for key, value in tickets.items():
    try:
        print('Getting: ' + key)
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
# get FX data, notice several parameters should be set or resp will be 404
try:
    h = httplib2.Http()    
    resp, content = h.request("http://www.m2j.co.jp/market/pchistry_dl.php?ccy=1&type=d", "GET", 
                              headers={"accept-encoding":"gzip, deflate", "accept-language":"zh,ja;q=0.8,en-US;q=0.6,en;q=0.4", "referer":"http://www.m2j.co.jp/market/historical.php"})
except:
    print("Using Proxy")
    h = httplib2.Http(
        proxy_info = httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_HTTP, 'proxy.mei.co.jp', 8080
            ) )
    resp, content = h.request("http://www.m2j.co.jp/market/pchistry_dl.php?ccy=1&type=m", "GET")

path = './data/FX/USDJPY/'
os.makedirs(path, exist_ok=True)

oFile = open(path + 'data.csv', 'wb')
oFile.write(content)
oFile.close()
print("FX: USDJPY Updated")

#--------------- BitCoin Data -------------------------
from BTCUpdate import updateCryptoCurrencyData
updateCryptoCurrencyData()