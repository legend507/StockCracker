import httplib2
import sys

def UpdateData(url, savePath):
    try:
        h = httplib2.Http()    
        resp, content = h.request(url, "GET")
    except:
        print("Using Proxy")
        h = httplib2.Http(
            proxy_info = httplib2.ProxyInfo(
                httplib2.socks.PROXY_TYPE_HTTP, 'proxy.mei.co.jp', 8080
                ) )
        resp, content = h.request(url, "GET")

    oFile = open(savePath, 'wb')
    oFile.write(content)
    oFile.close()

#---- get nikkei index data
try:
    h = httplib2.Http()    
    resp, content = h.request("http://k-db.com/indices/I101/1d/2017?download=csv", "GET")
except:
    print("Using Proxy")
    h = httplib2.Http(
        proxy_info = httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_HTTP, 'proxy.mei.co.jp', 8080
            ) )
    resp, content = h.request("http://k-db.com/indices/I101/1d/2017?download=csv", "GET")

oFile = open('./20151127_TOPIX/20151127_TOPIX/Nikkei/indices_I101_1d_2017.csv', 'wb')
oFile.write(content)
oFile.close()

#---- get Mazda data
try:
    h = httplib2.Http()    
    resp, content = h.request("http://k-db.com/stocks/7261-T/1d/2017?download=csv", "GET")
except:
    print("Using Proxy")
    h = httplib2.Http(
        proxy_info = httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_HTTP, 'proxy.mei.co.jp', 8080
            ) )
    resp, content = h.request("http://k-db.com/stocks/7261-T/1d/2017?download=csv", "GET")

oFile = open('./20151127_TOPIX/20151127_TOPIX/Mazda/stocks_7261-T_1d_2017.csv', 'wb')
oFile.write(content)
oFile.close()

#---- get Round1 data
try:
    h = httplib2.Http()    
    resp, content = h.request("http://k-db.com/stocks/4680-T/1d/2017?download=csv", "GET")
except:
    print("Using Proxy")
    h = httplib2.Http(
        proxy_info = httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_HTTP, 'proxy.mei.co.jp', 8080
            ) )
    resp, content = h.request("http://k-db.com/stocks/4680-T/1d/2017?download=csv", "GET")

oFile = open('./20151127_TOPIX/20151127_TOPIX/Round1/stocks_4680-T_1d_2017.csv', 'wb')
oFile.write(content)
oFile.close()

#---- get FX data
try:
    h = httplib2.Http()    
    resp, content = h.request("http://m2j.co.jp/market/pchistry_dl.php?ccy=1&type=d", "GET")
except:
    print("Using Proxy")
    h = httplib2.Http(
        proxy_info = httplib2.ProxyInfo(
            httplib2.socks.PROXY_TYPE_HTTP, 'proxy.mei.co.jp', 8080
            ) )
    resp, content = h.request("http://m2j.co.jp/market/pchistry_dl.php?ccy=1&type=d", "GET")

oFile = open('./20151127_TOPIX/20151127_TOPIX/fx/USDJPY/USDJPY.csv', 'wb')
oFile.write(content)
oFile.close()