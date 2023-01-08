import requests
from bs4 import  BeautifulSoup
import pandas
from fake_useragent import UserAgent
import matplotlib.pyplot as plt

def findPE(WhatStockWeWantToSee):
    src = 'https://concords.moneydj.com/z/zc/zca/zca_'+WhatStockWeWantToSee+'.djhtm'
    UA=UserAgent()
    headers={
        "User-Agent":UA.google
    }
    response = requests.get(src,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    # find waht we want
    Recentprice = soup.find('td' ,{'class' : 't4t1'} , string = '收盤價')
    high_PE = soup.find('td' ,{'class' : 't4t1'} , string = '最高本益比')
    low_PE = soup.find('td' ,{'class' : 't4t1'} , string = '最低本益比')
    # extract the price we want 
    Recentprice = Recentprice.find_next_siblings('td') # only one price
    high_PE = high_PE.find_next_siblings('td') # about eight years highest PE
    low_PE = low_PE.find_next_siblings('td') # about eight years lowest PE
    # print(Recentprice)
    # print(low_PE)
    average_PE = []
    for i in range(len(high_PE)):
        # print(float(high_PE[i].get_text()))
        # print(float(low_PE[i].get_text()))
        try:
            average = round( ( float(high_PE[i].get_text()) +  float(low_PE[i].get_text()) )/2  , 2)
            average_PE.append( average )
        except:
            continue
    
    year= 2023
    for i in average_PE:
        print(year , ' 平均本益比 : ' , i )
        year-=1
    
    # return averagePE and Todays Price
    return average_PE , float( Recentprice[0].get_text())

def findEPS(WhatStockWeWantToSee):
    src = 'https://histock.tw/stock/'+WhatStockWeWantToSee+'/%E6%AF%8F%E8%82%A1%E7%9B%88%E9%A4%98'
    UA=UserAgent()
    headers={
        "User-Agent":UA.google
    }
    response = requests.get(src,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    table = soup.find('th',string = '總計')
    table = table.find_next_siblings('td')
    EPS = []
    for i in table:
        try:
            EPS.append( float(i.get_text()))
        except:
            continue
    EPS.reverse()
    year= 2022
    for i in EPS:
        print(year , ' EPS : ' , i )
        year-=1
    return EPS 

def BuyOrNot(WhatStockWeWantToSee , TheFitPrices ,TodayPrice ):
    total_year = []
    year = 2022
    for i in TheFitPrices:
        total_year.append(year)
        print(year , ' 合理的價格可以購買 : ' , i )
        year-=1
    print('---------分隔線-------------')
    print('我們將最後可收購價格設置在合理股價的105%')
    # 我抓比平均價格高5%來當作一個最後可以收購的價格，如果低於這個就可以做購買
    if TheFitPrices[0]*1.05 >= TodayPrice:
        print('可收購股價算出來是 : ',TheFitPrices[0]*1.05 ,' >  現在的股價 : ' , TodayPrice)
        print("這個價格可以思考要不要購買!")
        plt.text(2016,TodayPrice+5,"You can buy it!!! ",fontsize =18 ,color = 'red')
    else:
        print('可收購股價算出來是 : ',TheFitPrices[0]*1.05 ,' < 現在的股價 : ' , TodayPrice)
        print('目前可能不是時候購買 因為本益比法告訴我們 目前不適合!')
        plt.text(2016,TodayPrice+5,"Do not but it!!!",fontsize =18 ,color = 'red' )

    # make pictrue
    plt.title(str(WhatStockWeWantToSee)+' Fitable Stock Price')
    plt.xlabel('Years')
    plt.ylabel('Prices')
    line1, = plt.plot(total_year,TheFitPrices,label = 'Fitable Prices',color = 'red' , marker='o')
    line2, = plt.plot(total_year[0],TodayPrice,label = 'TodayPrice',color = 'blue' , marker='o')
    plt.legend(handles = [line1,line2]  , loc='upper right') 
    plt.show()

    return total_year

# main function
if __name__ == '__main__':
    while(True):
        print('\n若不想查詢可以直接輸入 exit')
        WhatStockWeWantToSee = str(input('請輸入想查詢的股票號碼 : '))
        if WhatStockWeWantToSee=='exit':
            break
        print('您查詢的股票資訊',WhatStockWeWantToSee,'如下!')
        print()
        averagePE , TodayPrice = findPE(WhatStockWeWantToSee)
        print('---------分隔線-------------')
        EPS = findEPS(WhatStockWeWantToSee)
        print('----------分隔線------------')
        TheFitPrices = []
        for i in range(1, len(averagePE)):
            TheFitPrices.append( round(averagePE[i]*EPS[i-1], 2)   )
        total_year = BuyOrNot(WhatStockWeWantToSee,TheFitPrices , TodayPrice)
        print('-----------結束線---------\n')
        
# with open('stock.txt','ab') as f:
#     f.write(soup)
#     f.close()