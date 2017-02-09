import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import numpy as np
import matplotlib.mlab as mlab
import math
import matplotlib
import csv
import os.path
import datetime
# refer to the example in scikit-learn webpage!!!!
import sklearn 

rootpath = './'

def readCSV(fileName):
    file_path = os.path.join(rootpath, fileName)
    file = open(file_path)
    data = csv.reader(file, delimiter=',')
    return data

data2013 = readCSV('I102_2013.csv')
data2014 = readCSV('I102_2014.csv')
data2015 = readCSV('I102_2015.csv')

#####################################
# all data store in these arrays
dates   = []
starts  = []
highs   = []
lows    = []
ends    = []
#-----------------------------------#

def readData(dataName):
    dates_      =[]
    starts_     =[]
    highs_      =[]
    lows_       =[]
    ends_       =[]
    for row in dataName:
        date    = row[0]
        start   = row[1]
        high    = row[2]
        low     = row[3]
        end     = row[4]

        dates_.append(date)
        starts_.append(start)
        highs_.append(high)
        lows_.append(low)
        ends_.append(end)

    # setting the data chronicle
    dates_.reverse()
    starts_.reverse()
    highs_.reverse()
    lows_.reverse()
    ends_.reverse()

    dates.extend( dates_ )
    starts.extend( starts_ )
    highs.extend( highs_ )
    lows.extend( lows_ )
    ends.extend( ends_ )
    return

readData(data2013)
readData(data2014)
readData(data2015)

#################################
#   detect changing point
avg_before      = []
avg_after       = []
avg_around      = []
#   fill in the 3 lists
def detectChange(data_string):
    dataList = []
    for element in data_string:
        dataList.append( float(element) )
    boundry_before = 0
    boundry_after = 0
    for index in range(len(lows)):
        # decide upper boundry
        if index - 100 < 0:
            boundry_before = 0;
        else:
            boundry_before = index -100
        # decide lower boundry
        if index + 100 > len(lows):
            boundry_after = len(lows)
        else:
            boundry_after = index + 100

        avg_before.append( np.average(dataList[boundry_before:index]) )
        avg_after.append( np.average(dataList[index:boundry_after]) )
        avg_around.append( np.average(dataList[boundry_before:boundry_after]) )
    return
#--------------------------------#

detectChange(lows)

##############################
#   calculate weight
weights = []
def calcWeights(data_string):
    dataList = []
    for element in data_string:
        dataList.append( float(element) )

    for index in range(len(dataList)):
        if index == 0:
            weights.append(0)
        else:
            weights.append(dataList[index] - avg_before[index] + avg_around[index] -avg_after[index])
    return
#-----------------------------#
calcWeights(lows)

for index in range(len(weights)):
    weights[index] += math.fabs(min(weights))

###############################
#   make a-axis display date
x = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
#-----------------------------#

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gca().xaxis.set_visible(False)
plt.plot(x, starts,     label='starts')
plt.plot(x, highs,      label='highs')
plt.plot(x, lows,       label='lows')
plt.plot(x, ends,       label='ends')
plt.plot(x, weights,    label='weights')
plt.gcf().autofmt_xdate()
plt.title('TOPIX Analysis')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc=5)
plt.grid()
plt.show()