import httplib2
h = httplib2.Http()
resp, content = h.request("http://k-db.com/indices/I101/1d/2017?download=csv", "GET")


oFile = open('./test.csv', 'w')
oFile.write(content)
oFile.close()