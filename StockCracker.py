import numpy as np
np.set_printoptions(threshold=np.nan)
import pandas as pd
import datetime
import os

#---- for statistics
from scipy import stats

class LabelManager:
    def __init__(self):
        self.DATE = 'Date'
        self.OPEN = 'Open'
        self.HIGH = 'High'
        self.LOW  = 'Low'
        self.CLOSE = 'Close'
        self.VOLUME = 'Volume'
label = LabelManager()

TOOLTIPS = [
    (label.DATE, '$1'),
    (label.OPEN, '$2'),
]

class StockCracker:
    def __init__(self):
        
        self.label = LabelManager()
        print("Initializing StockCracker instance")
        
    def readOneCsv_Yahoo(self, filePath):
        data = pd.read_csv(filePath, encoding='UTF-8', header=0)
        data[label.DATE] = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in data[label.DATE]]
        data[label.OPEN] = pd.to_numeric(data[label.OPEN], errors='coerce')
        data[label.HIGH] = pd.to_numeric(data[label.HIGH], errors='coerce')
        data[label.LOW] = pd.to_numeric(data[label.LOW], errors='coerce')
        data[label.CLOSE] = pd.to_numeric(data[label.CLOSE], errors='coerce')
        data[label.VOLUME] = pd.to_numeric(data[label.VOLUME], errors='coerce')
        return data
        
    # read one csv file
    def readOneCsv(self, filePath, isReversed):
        '''
        Obsolete, do NOT use this API
        '''
        data = pd.read_csv(filePath, encoding='shift-JIS', header=0)
        if isReversed is True:
            data = data.reindex(index=data.index[::-1])
            data.index = range(len(data))
        #print(Fore.YELLOW + data['日付'][0] + '~' + data['日付'][len(data)-1])
        return data

    # read one folder, recurssively
    def readOneFolder(self, folderPath, isReversed=True):
        '''
        Obsolete, do NOT use this API
        '''
        for root, subdirs, files in os.walk(folderPath):
            #print('----------------')
            #print(Back.CYAN + Fore.RED + Style.BRIGHT + 
            #      'In Folder:'+root)
            #---- sorted() here sorts files 
            for oneCsv in sorted(files):
                #print(Back.CYAN +"    "+ oneCsv)
                filePath = folderPath+oneCsv
                data = self.readOneCsv(filePath, isReversed)
                try:
                    allData
                except NameError:   # allData not exist
                    allData = data
                else:   # allData exist
                    # concatenate 2 pandas dataframes
                    allData = pd.concat([allData, data])
        allData.index = range(len(allData))
        #print(allData) # output all data of target stock
        return allData

    # calculate Beta coefficient, 
    def calcBetaCoefficient(self, stock, index):
        #---- 
#### following example gives a good intuition about the quantitative  
#        >>> a = np.array([1,3,9,6,5])
#        >>> b = a + 100
#        >>> b
#        array([101, 103, 109, 106, 105])
#        >>> np.cov(a,b,bias=1)
#        array([[ 7.36,  7.36],
#                [ 7.36,  7.36]])
#        >>> b = a * 10
#        >>> np.cov(a,b,bias=1)
#        array([[   7.36,   73.6 ],
#               [  73.6 ,  736.  ]])
        # clean data, stock and index should have same date time before calculation
        sharedDate = list(set(stock[self.label.DATE]).intersection(index[self.label.DATE]))
        stock = stock[stock[self.label.DATE].isin(sharedDate)]
        index = index[index[self.label.DATE].isin(sharedDate)]
        # calculate daily change of stock and index
        dailyChange_stock = np.array([(stock.iloc[idx+1][self.label.CLOSE] - stock.iloc[idx][self.label.CLOSE]) / stock.iloc[idx][self.label.CLOSE] for idx in range(len(stock) - 1)]) # from 0 ~ len(stock)-1
        dailyChange_index = np.array([(index.iloc[idx+1][self.label.CLOSE] - index.iloc[idx][self.label.CLOSE]) / index.iloc[idx][self.label.CLOSE] for idx in range(len(index) - 1)]) # from 0 ~ len(index)-1
        # covariance matrix(a, b) = 
        # [[var(a)    cov(a, b)]
        #  [cov(b, a) var(b)   ]]
        #
        matrix = np.cov(dailyChange_stock, dailyChange_index, bias=1)        
        beta = matrix[0][1] / matrix[1][1]
        print("Beta = {}".format(beta))
        if beta > 1:
            print("Target Stock is MORE volitale than the index, target stock is RISKY")
        else:
            print("Target Stock is LESS volitale than the index, target stock is NOT risky")
        return beta, dailyChange_stock, dailyChange_index
    
    # On-balance volume, need 出来高 of the target stock
    def keyIndicator_OBV(self, stock):
        OBV = np.zeros(len(stock))
        OBV[0] = 0 
        for idx in range(len(stock)):
            if idx == 0:
                pass
            if stock[self.label.CLOSE].iloc[idx] > stock[self.label.CLOSE].iloc[idx - 1]:
                OBV[idx] = OBV[idx - 1] + stock[self.label.VOLUME].iloc[idx]
            elif stock[self.label.CLOSE].iloc[idx] < stock[self.label.CLOSE].iloc[idx - 1]:
                OBV[idx] = OBV[idx - 1] - stock[self.label.VOLUME].iloc[idx]
            else:
                OBV[idx] = OBV[idx - 1]
        return OBV
    #-- MACD
    #----- Simple moving average
    def calc_SMA(self, stock, N):
        SMA = np.zeros(len(stock))
        for i in range(len(stock)):
            if i > N-2:
                """Why N-2? 
                e.g., if N=10, need to sum day0~day9, therefore need to begin from i=9 (aka.i>10-2=8)
                """
                SMA[i] = stock[self.label.CLOSE][i-N+1:i].sum() / N
        return SMA
    #----- Exponential moving average
    def calc_EMA(self, stock, N):
        SMA = self.calc_SMA(stock, N)
        EMA = np.zeros(len(stock))
        EMA[N-1] = SMA[N-1]             # EMA_0 value
        multiplier = 2 / (N + 1)
        for i in range(len(stock)):
            if i > N - 1:
                EMA[i] = multiplier * (stock[self.label.CLOSE].iloc[i] - EMA[i-1]) + EMA[i-1]
        return EMA
    #----- MACD and signal
    def keyIndicator_MACD(self, stock, N1, N2, sigN):
        EMA_N1 = self.calc_EMA(stock, N1)
        EMA_N2 = self.calc_EMA(stock, N2)
        MACD   = EMA_N1 - EMA_N2
        #--- zerolize all necessary index
        if N1 < N2:
            border = N2 - 1
        else:
            border = N1 - 1
        for idx in range(border):
            MACD[idx] = 0
        #--- calc Signal line
        multiplier = 2/(sigN + 1)
        signal = np.zeros(len(stock))
        signal[border+sigN-1] = np.average( MACD[border:border+sigN-1] )
        for idx in range(border+sigN, len(stock)):
            signal[idx] = MACD[idx] * multiplier + signal[idx-1] * (1 - multiplier)
        return MACD, signal
    #-------------
    # 我需要分析index以及之前N天，之后M天的数据～
    #-------------
    def focusOn(self, stock, index, formerN, laterM):
        start = index - formerN
        if start < 0:
            start = 0
            
        end = index + laterM
        if end > stock.size:
            end = len(stock)
        return stock[start:end]
    #-------------
    # 计算LinearRegression [WIP]
    #-------------
    def calcSlope(self, data):
        return
    
    #-------------    
    # Relative strength index, 
    #-------------
    def keyIndicator_RSI(self, stock, N=14):
        # create an array
        RSI = np.full(len(stock), 100.)
        # calculate RSI_0 for first N days
        gain = 0
        loss = 0
        for i in range(N):
            today = stock[self.label.CLOSE].iloc[i] - stock[self.label.OPEN].iloc[i]
            # closs >= open, gain
            if today >= 0:
                gain += today
            else:
                loss -= today
        avg_gain = gain / N
        avg_loss = loss / N
        if avg_loss != 0:
            RSI[N] = 100 - 100 / (1 + avg_gain / avg_loss)
        
        # calculate the following 
        for i in range(N+1, len(stock)):
            today = stock[self.label.CLOSE].iloc[i] - stock[self.label.OPEN].iloc[i-1]
            if today >= 0:
                avg_gain = (avg_gain * 13 + today) / 14
                avg_loss = (avg_loss * 13 + 0) / 14
            else:
                avg_gain = (avg_gain * 13 + 0) / 14
                avg_loss = (avg_loss * 13 - today) / 14
            if avg_loss != 0:
                RSI[i] = 100 - 100 / (1 + avg_gain / avg_loss)
        return RSI