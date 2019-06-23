import pandas_datareader as web
from datetime import datetime

start_date = datetime(2000, 1, 1)
end_date = datetime.today()
jpy = web.DataReader('DEXJPUS', 'fred', start=datetime(2000, 1, 1), end=datetime.today())

print(jpy)