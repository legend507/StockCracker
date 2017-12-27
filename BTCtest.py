import pandas as pd
from datetime import datetime

df = pd.read_csv("./20151127_TOPIX/20151127_TOPIX/Bitcoin/test.csv",
                 header=None,
                 parse_dates=True,
                 date_parser=lambda x: datetime.fromtimestamp(float(x)),
                 index_col='datetime',
                 names=['datetime', 'price', 'amount'])
df["price"].plot()

df.to_csv('./20151127_TOPIX/20151127_TOPIX/Bitcoin/BTC.csv')
