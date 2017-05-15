import httplib2
import sys

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

oFile = open('./test.csv', 'wb')
oFile.write(content)
oFile.close()