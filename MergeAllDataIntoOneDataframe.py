from updateData import Tickers
from StockCracker import StockCracker
from StockCracker import LabelManager

allStock = Tickers()
sc = StockCracker()

for name, value in allStock.tickers.items():
    print('{}: {}'.format(name, value))
    df = sc.readOneCsv_Yahoo(value + 'data.csv')
    df.columns = [value[13:-1] + '-' + x for x in df.columns ]
    print(df.head())