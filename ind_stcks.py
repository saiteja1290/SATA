
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
        message='Possible Sell Signal , Please Check The Stock  - {0}'.format(
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
def golden_strat(code):
    a = movingaverage(code, 20)
    b = movingaverage(code, 50)
    if(a > b):
        if(round(movingaverage(code, 20)) == round(movingaverage(code, 50))):
            sell(code)
    else:
        if(round(movingaverage(code, 20), -1) == round(movingaverage(code, 50), -1)):
            buy(code)
def strat_2(code):
    a = movingaverage(code, 5)
    b = movingaverage(code, 20)
    if(a > b):
        if(round(movingaverage(code, 5)) == round(movingaverage(code, 20))):
            sell(code)
    else:
        if(round(movingaverage(code, 5), -1) == round(movingaverage(code, 20), -1)):
            buy(code)
            
def rsistart(code):
    if(rsi(code) <= 35):
        buy(code)
    if(rsi(code) >= 65):
        sell(code)

def main():
    while(True):
        golden_strat('reliance-industries')
        golden_strat('tata-consultancy-services')
        golden_strat('hdfc-bank-ltd')
        golden_strat('infosys')
        golden_strat('hindustan-unilever')
        golden_strat('icici-bank-ltd')
        golden_strat('state-bank-of-india')
        golden_strat('housing-development-finance')
        golden_strat('bharti0-airtel')
        golden_strat('itc')
        # strat_2('infosys')
        sleep(10)
main()