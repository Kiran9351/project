
import pandas as pd
import numpy as np
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt
import math

def get_ticker(stock_name):
	df = pd.read_csv('Company_names.csv')
	symbol = df['Symbol'].tolist()
	company = df['Company'].tolist()
	ticker_idx = company.index(stock_name)

	return symbol[ticker_idx]


def check_data_continuation(stock_name,date):
	name = stock_name.replace(' ','_')
	data = pd.read_csv(name+'.csv')

	last_date = data[0][len(data['Date']) - 1]
	end_date = datetime.now()


	if(last_date <= date):

		ticker = get_ticker(stock_name)
		df = yf.download(stock_name, last_date, end_date)
		data.drop(data.tail(1).index, inplace = True)
		data = pd.concat([data,df],axis = 0)
		data.to_csv(stock_name+'.csv')
		return  data

	else:
		return data 


def attach_log_column(data):
	log_column = [0]
	#adj_column = data['Adj Close'].tolist()
	adj_column = data['Close'].tolist()
	#print(adj_column)

	for i in range(1,len(adj_column)):
		div_val = adj_column[i]/adj_column[i-1]
		log_column.append(math.log(div_val) * 100)

	data = data.assign(Log_Column=log_column)
	#data.head()

	return data


def Look_for_stats(stock_name, start_date):

	data = check_data_continuation(stock_name,start_date)

	#print(type(data))

	data = attach_log_column(data)

	print("Printing last 5 rows of data:\n\n")
	print(data.head(n = 5))
	print("\n\n\n")

	option = 'y'

	while(option == 'y'):
		print("1 : To look for graph of open values : ")
		print("2 : To look for graph of close values : ")
		print("3 : To look for graph of high values : ")
		print("4 : To loof for graph of close values : ")
		print("5 : To look for graph of adjusted close price values : ")
		print("6 : To look for graph of volume : ")
		print("7 : To graph log column : ")

		choose = int(input("Choose the option above: "))

		if(choose == 1):
			data['Open'].plot(figsize = (10,7))
			
			plt.title("Open prices of %s"% ticker, fontsize = 16)
			
			plt.ylabel("Price",fontsize = 14)
			plt.xlabel("Year",fontsize = 14)

			plt.grid(which = 'major',linestyle = '-.',linewidth = 0.5)

			plt.show()

		elif(choose == 2):
			data['Close'].plot(figsize = (10,7))
			
			plt.title("Clsed prices of %s"%ticker, fontsize = 16)
			
			plt.ylabel("Price",fontsize = 14)
			plt.xlabel("Year",fontsize = 14)

			plt.grid(which = 'major',linestyle = '-.',linewidth = 0.5)

			plt.show()

		elif(choose == 3):
			data['High'].plot(figsize = (10,7))
			
			plt.title("Highes prices of %s"%ticker, fontsize = 16)
			
			plt.ylabel("Price",fontsize = 14)
			plt.xlabel("Year",fontsize = 14)

			plt.grid(which = 'major',linestyle = '-.',linewidth = 0.5)

			plt.show()

		elif(choose == 4):
			data['Low'].plot(figsize = (10,7))
			
			plt.title("Lowest prices of %s"%ticker, fontsize = 16)
			
			plt.ylabel("Price",fontsize = 14)
			plt.xlabel("Year",fontsize = 14)

			plt.grid(which = 'major',linestyle = '-.',linewidth = 0.5)

			plt.show()

		elif(choose == 5):
			data['Adj Close'].plot(figsize = (10,7))
			
			plt.title("Adjusted close prices of %s"%ticker, fontsize = 16)
			
			plt.ylabel("Price",fontsize = 14)
			plt.xlabel("Year",fontsize = 14)

			plt.grid(which = 'major',linestyle = '-.',linewidth = 0.5)

			plt.show()

		elif(choose == 6):
			data['Volume'].plot(figsize = (10,7))
			
			plt.title("Volumes of  %s"%ticker, fontsize = 16)
			
			plt.ylabel("Volume",fontsize = 14)
			plt.xlabel("Year",fontsize = 14)

			plt.grid(which = 'major',linestyle = '-.',linewidth = 0.5)

			plt.show()

		else:
			data['Log_Column'].plot(figsize = (10,7))
			plt.title("Log Values of %s"%ticker, fontsize = 16)

			plt.ylabel("Log values",fontsize = 14)
			plt.xlabel("Year",fontsize=14)

			plt.grid(which = 'major',linestyle = '-.', linewidth = 0.5)

			plt.show()


		option = input("Do you want to see other graphs? if yes enter 'y' else 'n' : ")







option = 'y'

while(option == 'y'):

	print("1 : Stats of single stock")
	print("2 : Compare two stocks")

	choice = int(input("Enter your choice : "))

	if(choice == 1):
		stock_name = input('Enter stock name : ')
		start_date = input("Enter start date in yyyy-mm-dd : ")

		Look_for_stats(stock_name, start_date)

	else:
		Compare_two_stock()