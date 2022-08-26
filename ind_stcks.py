
from math import floor
import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from plyer import notification

stockpricelist = []
def strtoflt(str):
    newstr = ''
    for i in range(len(str)):
        if(str[i] == ','):
            pass
        else:
            newstr += str[i]
    return float(newstr)
def buy(code):
    notification.notify(
        title='Notification',
        message='Possible Buy Signal , Please Check The Stock  - {0}'.format(
            code),
        app_icon=None,
        timeout=10,
    )
def sell(code):
    notification.notify(
        title='Notification',
        message='Possible Sell Signal , Please Check The Stock  - {0}'.format(
            code),
        app_icon=None,
        timeout=10,
    )
def stockprice(code):
    # lowercase = str(code).lower
    url = 'https://in.investing.com/equities/{0}'.format(code)
    r = requests.get(url)

    stockpricelol = BeautifulSoup(r.text, 'html5lib')
    stockpricelol = stockpricelol.find('div', {'class': 'last u-up'})
    stockpricelol = stockpricelol.find('bdo').text
    stockpricelist.append(strtoflt(stockpricelol))

    return strtoflt(stockpricelol)
def movingaverage(code, lenght):
    url = 'https://in.investing.com/equities/{0}-technical'.format(code)
    r = requests.get(url)

    l = []
    ma = BeautifulSoup(r.text, 'html5lib')
    ma = ma.find_all('span')
    count = 0
    count2 = 0
    for i in ma:
        if(i.text == 'MA{0}'.format(lenght)):
            # print((i).text)
            count += 1
        if(count == 1):
            # print(i.text,end = ' ')
            l.append(i.text)
            count2 += 1
            if(count2 == 2):
                break
    return strtoflt(l[1])
def rsi(code):
    url = 'https://in.investing.com/equities/{0}-technical'.format(code)
    r = requests.get(url)
    l = []
    stockpricelol = BeautifulSoup(r.text, 'html5lib')
    stockpricelol = stockpricelol.find_all('span')
    count = 0
    count2 = 0
    for i in stockpricelol:
        if(i.text == 'RSI(14)'):
            # print((i).text)
            count += 1
        if(count == 1):
            # print(i.text,end = ' ')
            l.append(i.text)
            count2 += 1
            if(count2 == 2):
                break
    return strtoflt(l[1])
def strat1(code):
    ma50 = movingaverage(code,50)
    ma20 = movingaverage(code,20)
    ma5 = movingaverage(code,5)
    if(ma50 < stockprice(code)):
        if(ma5 < ma20):
            if(round(ma5,-1) == round(ma20,-1)):
                buy(code)
        elif(ma20 < ma5):
            if(round(ma5,-1) == round(ma20,-1)):
                sell(code)
