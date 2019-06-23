"""This script merge all downloaded stock data into one large pandas dataframe. 
"""

from updateData import Tickers
from StockCracker import StockCracker
from StockCracker import LabelManager

import pandas as pd

allStock = Tickers()
sc = StockCracker()

# create empty dataframe to hold all data
agg_df = pd.DataFrame()

# traverse all tickers defined in updateData.py, and merge the dfs into one df
for name, value in allStock.tickers.items():
    print('{}: {}'.format(name, value))
    df = sc.readOneCsv_Yahoo(value + 'data.csv')
    df.columns = ['Date'] + [value[13:-1] + '-' + x for x in df.columns if x != 'Date']
    if (agg_df.empty):
        agg_df = df
    else:
        # by specifing how='outer', the aggregated df keeps rows with no values
        agg_df = pd.merge(agg_df, df, on='Date', how='outer')
    
agg_df.to_csv('./data/stock_aggregated.csv')