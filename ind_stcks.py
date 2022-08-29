
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
def alert(code):
    notification.notify(
        title='Notification',
        message='alert Signal , Please Check The Stock  - {0}'.format(
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
    stockpricelol = stockpricelol.find('bdo', {'class': 'last-price-value js-streamable-element'}).text
    # stockpricelol = stockpricelol.find('bdo').text
    # stockpricelist.append(strtoflt(stockpricelol))

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
    stk = stockprice(code)
    if(stk>ma50):
        if(len(str(stk))==3):
            if(round(ma5) == round(ma20)):
                alert(code)
        elif(len(str(stk)) == 4):
            if(round(ma5,-1) == round(ma20,-1)):
                alert(code)
def main():
    while(True):
        strat1('state-bank-of-india')
        strat1('reliance-industries')
        strat1('hdfc-bank-ltd')
        strat1('icici-bank-ltd')
        strat1('tata-steel')
        strat1('infosys')
        strat1('bank-of-baroda')
        strat1('axis-bank')
        strat1('kotak-mahindra-bank')
        strat1('hindustan-unilever')
        strat1('hindalco-industries')
        strat1('indian-oil-corporation')
        strat1('wipro-ltd')
        strat1('tata-motors-ltd')
        strat1('itc')
        strat1('coal-india')
        strat1('bharat-heavy-electricals')
        strat1('the-federal-bank')
        strat1('bharti-airtel')
        strat1('adani-enterprises')
        strat1('adani-power')
main()
# print(stockprice('reliance-industries'))   
# print(type(stockprice('reliance-industries')))
