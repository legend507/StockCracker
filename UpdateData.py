import httplib2
h = httplib2.Http(".cache")
resp, content = h.request("http://k-db.com/indices/I101/1d/2017?download=csv", "GET")

print(content)