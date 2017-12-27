import pandas as pd
from datetime import datetime

df = pd.read_csv("http://api.bitcoincharts.com/v1/trades.csv?symbol=coincheckJPY",
                 header=None,
                 parse_dates=True,
                 date_parser=lambda x: datetime.fromtimestamp(float(x)),
                 index_col='datetime',
                 names=['datetime', 'price', 'amount'])
df["price"].plot()