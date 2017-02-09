import pandas as pd
import numpy as np
import matplotlib
import datetime
from matplotlib import pyplot as plt
import seaborn as sns
import os
sns.set(style='ticks')

from colorama import init
init(autoreset=True)
from colorama import Fore, Back, Style

class StockCracker:
    def __init__(self):
        self.rootPath = './'
        self.USDJPYPath = './fx/USDJPY/'
        self.mazdaPath = './Mazda/'
        self.nikkeiPath = './Nikkei/'

    # read one csv file
    def readOneCsv(self, filePath, isReversed):
        data = pd.read_csv(filePath, encoding='shift-JIS', header=0)
        if isReversed is True:
            data = data.reindex(index=data.index[::-1])
            data.index = range(len(data))
        print(Fore.YELLOW + data['日付'][0] + '~' + data['日付'][len(data)-1])
        return data

    # read one folder, recurssively
    def readOneFolder(self, folderPath, isReversed=True):
        for root, subdirs, files in os.walk(folderPath):
            print('----------------')
            print(Back.CYAN + Fore.RED + Style.BRIGHT + 
                  'In Folder:'+root)
            for oneCsv in files:
                print(Back.CYAN + oneCsv)
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

if __name__ == '__main__':

    sc = StockCracker()
    # reading data ------------------------------------
    data_Nikkei = sc.readOneFolder(sc.nikkeiPath)
    data_Mazda  = sc.readOneFolder(sc.mazdaPath)
    data_fx     = sc.readOneFolder(sc.USDJPYPath, False)
    ## convert date
    date_Mazda    = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in data_Mazda['日付'][:]]
    date_Nikkei   = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in data_Nikkei['日付'][:]]
    date_fx       = [datetime.datetime.strptime(d, '%Y/%m/%d').date() for d in data_fx['日付'][:]]
    ### for Mazda, 2014-07-29 株併合:1株 -> 0.2株
    index = data_Mazda.loc[data_Mazda['日付'] == '2014-07-28'].index[0]
    data_Mazda['始値'][0:(index+1)] = data_Mazda['始値'][0:(index+1)] * 5
    
    # plot data ----------------------------------------
    fig, (ax, bx) = plt.subplots(2, sharex = True)
    ## Nikkei
    ax.plot(date_Nikkei, data_Nikkei['始値'][:], c='r')
    ax.set_ylabel('Nikkei', color='r', fontsize=20)
    ## Mazda
    ax1 = ax.twinx()
    ax1.plot(date_Mazda, data_Mazda['始値'][:], c='b')
    ax1.set_ylabel('Mazda', color='b', fontsize=20)
    ## fx USDJPY
    bx.plot(date_fx, data_fx['始値'][:], c='c')
    bx.set_ylabel('USDJPY', color='c', fontsize=20)

    plt.show()
