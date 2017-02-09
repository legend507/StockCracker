import pandas as pd
import numpy as np
import matplotlib
import datetime
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style='ticks')

class StockAnalyst:
    def __init__(self):
        self.NikkeiIndexPath = './Nikkei/'
        #self.targetStockPath = './Round1/'
        self.targetStockPath = './Mazda/'


    def readNikkei(self, fileName):
        file_path = self.NikkeiIndexPath + fileName
        data = pd.read_csv(file_path, encoding='shift-JIS', header=-1)
        data = data[1:]
        return (data.iloc[::-1]).as_matrix()

    def readTargetStock(self, fileName):
        file_path = self.targetStockPath + fileName
        data = pd.read_csv(file_path, encoding='shift-JIS', header=-1)
        data = data[1:]
        return (data.iloc[::-1]).as_matrix()
    
    def betaCoefficient(self, r_asset, r_benchmark):
        # var = sum((x_i - x_mean)^2)/N
        # cov = sum((x_i - x_mean)*(y_i - y_mean)) / (N-1)
        covMatrix = np.cov(r_asset, r_benchmark, bias = False)
        print(covMatrix)
        beta = covMatrix[0][1] / covMatrix[1][1]
        return beta

if __name__ == '__main__':
    round1Analyst = StockAnalyst()
    dataNikkei = round1Analyst.readNikkei('indices_I101_1d_2016.csv')
    dataRound1 = round1Analyst.readTargetStock('stocks_7261-T_1d_2016.csv')

    ## data format transform for plot
    # Round1
    round1_date     = dataRound1[:,0]               # YYYY-MM-DD format
    round1_date_plt = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in round1_date]
    round1_start    = (dataRound1[:,1]).astype(float)              # to float type
    round1_end      = (dataRound1[:,4]).astype(float)           
    round1_high     = (dataRound1[:,2]).astype(float)
    round1_stock    = (dataRound1[:,5]).astype(float) 
    round1_price    = (dataRound1[:,6]).astype(float)
    round1_return   = round1_end - round1_start
    # Nikkei
    nikkei_date     = dataNikkei[:,0]               # YYYY-MM-DD format
    nikkei_date_plt = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in nikkei_date]
    nikkei_start    = (dataNikkei[:,1]).astype(float)              # to float type
    nikkei_end      = (dataNikkei[:,4]).astype(float)
    nikkei_return   = nikkei_end - nikkei_start

    ## figure to plot Nikkei & Round1 
    fig, (ax, bx) = plt.subplots(2, sharex = True)
    # Nikkei date - start
    ax.scatter(nikkei_date_plt, nikkei_start, c='r')
    ax.plot(nikkei_date_plt, nikkei_start, c='r')
    ax.set_ylabel('Nikkei', color ='r', fontsize = 20)
    # Round1 date - start
    ax1 = ax.twinx()
    ax1.scatter(round1_date_plt, round1_start, c='b')
    ax1.plot(round1_date_plt, round1_start, c='b')
    ax1.set_ylabel('Round1', color = 'b', fontsize = 20)
    # figure for Round1 other attributes
    bx.bar(round1_date_plt, round1_price)
    bx.set_xlabel('Date')
    bx1 = bx.twinx()
    bx1.plot(round1_date_plt, round1_stock, c='r')
    
    ## figure to plot beta coefficient
    #nikkei_return = (nikkei_return - np.mean(nikkei_return)) / np.std(nikkei_return)
    #round1_return = (round1_return - np.mean(round1_return)) / np.std(round1_return)
    barWidth = 0.35
    fig, ax = plt.subplots()
    ax.bar(np.arange(len(nikkei_date_plt)), nikkei_return, barWidth, color='r')
    limit = (np.absolute(nikkei_return)).max()
    ax.set_ylim([-limit, limit])
    ax.set_ylabel('Nikkei', color='r', fontsize=20)
    ax1 = ax.twinx()
    ax1.bar(np.arange(len(round1_date_plt))+barWidth, round1_return, barWidth, color='b')
    limit = (np.absolute(round1_return)).max()
    ax1.set_ylim([-limit, limit])
    ax1.set_ylabel('Round1', color='b', fontsize=20)

    beta = round1Analyst.betaCoefficient(round1_return, nikkei_return)
    print(beta)

    plt.show()
