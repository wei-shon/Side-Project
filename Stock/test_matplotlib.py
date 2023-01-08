import matplotlib.pyplot as plt
averagePE = [ 21.77, 30.68, 23.4, 21.28, 17.99, 16.32, 14.2]
EPS = [7.79, 23.01, 19.97, 13.32, 13.54, 13.23, 12.89]
prices = [604.99, 705.95, 467.3, 283.45, 243.58, 215.91, 183.04]
years = [2022,2021,2020,2019,2018,2017,2016]

plt.title('The Fitable Stock Price')
plt.ylabel('Years')
plt.xlabel('Prices')
line1, = plt.plot(years,prices,label = 'Prices',color = 'red' , marker='o')
# line2, = plt.plot(years,averagePE , label = 'AveragePE',color = 'blue' , marker='o')
# line3, = plt.plot(years , EPS  ,label = 'EPS',color = 'orange' , marker='o')
# plt.legend(handles = [line1,line2,line3]  , loc='upper right') 
plt.legend(handles = [line1]  , loc='upper right') 
plt.show()