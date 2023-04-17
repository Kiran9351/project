import pandas as pd 
import math
import yfinance as yf
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
##%matplotlib inline 

###############################################################

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

 

###############################################################

def Look_for_stats(stock_name):

	start_date = input("Enter start date in yyyy-mm-dd : ")
	end_date = datetime.now()

	ticker = stock_name

	data = yf.download(ticker,start_date,end_date)

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

#################################################################

def Compare_2_stocks(first_stock,second_stock):

	start_date = input("Enter start date in yyyy-mm-dd : ")
	end_date = datetime.now()

	ticker1 = first_stock
	first_data = yf.download(ticker1,start_date,end_date)
	
	ticker2 = second_stock
	second_data = yf.download(ticker2,start_date,end_date)

	first_data = attach_log_column(first_data)
	second_data = attach_log_column(second_data)

	print("Last few rows of first stock data :\n\n")
	print(first_data.head(n = 5))
	print("\n\n\n")

	print("Last few row of second stock data : \n\n")
	print(second_data.head(n = 5))
	print("\n\n\n")

	option = 'y'

	while(option == 'y'):

		print("1 : To compare Open prices\n")
		print("2 : To comare high prices\n")
		print("3 : To compare low prices\n")
		print("4 : To compare close prices\n")
		print("5 : To compare adjusted close prices\n")
		print("6 : To compare Volumes\n")
		print("7 : Correlation between adjusted close prices")
		print("8 : Correlation between log values: ")
		print("9 : Plot log values: ")

		choose = int(input("Enter your option : "))

		if(choose == 1):
			first_data['Open'].plot(color = 'red', label = first_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))
			second_data['Open'].plot(color = 'blue', label = second_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))

			plt.title(first_stock + 'vs' + second_stock + '[Open Prices]', fontsize = 16)

			plt.xlabel("Price",fontsize = 14)
			plt.ylabel("Year",fontsize = 14)

			plt.legend()
			plt.show()

		elif(choose == 2):
			first_data['High'].plot(color = 'red', label = first_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))
			second_data['High'].plot(color = 'blue', label = second_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))

			plt.title(first_stock + 'vs' + second_stock + '[Highest Prices]', fontsize = 16)

			plt.xlabel("Price",fontsize = 14)
			plt.ylabel("Year",fontsize = 14)

			plt.legend()
			plt.show()

		elif(choose == 3):
			first_data['Low'].plot(color = 'red', label = first_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))
			second_data['Low'].plot(color = 'blue', label = second_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))

			plt.title(first_stock + 'vs' + second_stock + '[Low Prices]', fontsize = 16)

			plt.xlabel("Price",fontsize = 14)
			plt.ylabel("Year",fontsize = 14)

			plt.legend()
			plt.show()

		elif(choose == 4):
			first_data['Close'].plot(color = 'red', label = first_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))
			second_data['Close'].plot(color = 'blue', label = second_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))

			plt.title(first_stock + 'vs' + second_stock + '[Close Prices]', fontsize = 16)

			plt.xlabel("Price",fontsize = 14)
			plt.ylabel("Year",fontsize = 14)

			plt.legend()
			plt.show()

		elif(choose == 5):
			first_data['Adj Close'].plot(color = 'red', label = first_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))
			second_data['Adj Close'].plot(color = 'blue', label = second_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))

			plt.title(first_stock + 'vs' + second_stock + '[Adj Close Prices]', fontsize = 16)

			plt.xlabel("Price",fontsize = 14)
			plt.ylabel("Year",fontsize = 14)

			plt.legend()
			plt.show()

		elif(choose == 6):
			first_data['Volume'].plot(color = 'red', label = first_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))
			second_data['Volume'].plot(color = 'blue', label = second_stock, linestyle = '-.', linewidth = 0.5, figsize = (10,7))

			plt.title(first_stock + 'vs' + second_stock + '[Volume Prices]', fontsize = 16)

			plt.xlabel("Price",fontsize = 14)
			plt.ylabel("Year",fontsize = 14)

			plt.legend()
			plt.show()

		elif(choose == 7):

			print(first_data['Adj Close'].corr(second_data['Adj Close']))

			x = tuple(first_data['Adj Close'].tolist())
			y = tuple(second_data['Adj Close'].tolist())

			plt.scatter(x,y)
			plt.xlabel(first_stock,fontsize = 14)
			plt.ylabel(second_stock,fontsize = 14)

			plt.show()

		elif(choose == 8):

			log_1 = first_data['Log_Column'].tolist()
			log_2 = second_data['Log_Column'].tolist()

			m_1 = sum(log_1)/len(log_1)
			m_2 = sum(log_2)/len(log_2)

			numerator = 0
			for i in range(len(log_1)):
				numerator += ((log_1[i] - m_1) * (log_2[i] - m_2))


			denom_1 = 0
			denom_2 = 0

			for j in range(len(log_1)):

				denom_1 += ((log_1[j] - m_1) * (log_1[j] - m_1))
				denom_2 += ((log_2[j] - m_2) * (log_2[j] - m_2))

			denominator = denom_1 * denom_2

			print("Correlation is ",numerator/denominator)

		elif(choose == 9):
			first_data['Log_Column'].plot(label = first_stock,figsize = (10,7))
			second_data['Log_Column'].plot(label = second_stock,figsize = (10,7))

			plt.title(first_stock + "vs" + second_stock + "[Log_Column]", fontsize = 16)

			plt.xlabel("Year",fontsize = 14)
			plt.ylabel("Log values", fontsize = 14)
			second_data.to_csv(second_stock+".csv")

			plt.legend()
			plt.show()

		else:
			first_data['Close'].plot(label = first_stock,figsize = (10,7))
			second_data['Close'].plot(label = second_stock,figsize = (10,7))

			plt.title(first_stock + "vs" + second_stock + "[Close]", fontsize = 16)

			plt.xlabel("Year",fontsize = 14)
			plt.ylabel("Close values", fontsize = 14)
			second_data.to_csv(second_stock+".csv")

			plt.legend()
			plt.show()


		option = input("Do you want to see other graphs? if yes enter 'y' else 'n' : ")



###############################################################


def correlation_heatmap_of_adj_close(list_of_stocks):
	df = pd.DataFrame()

	dataframes = []

	start_date = input("Enter start date : ")
	end_date = datetime.now() #input("Enter end date : ")

	for i in range(len(list_of_stocks)):
		data = yf.download(list_of_stocks[i], start_date, end_date)
		#dataframes.append(data)
		# print(data.head(n = 3))
		# print("\n\n\n")
		adj_column = data['Adj Close']
		#df = df.join(adj_column)
		df.insert(i,list_of_stocks[i], adj_column)

	df_corr = df.corr()

	#print(df_corr.head(n = 5))

	df_corr_plot = sns.heatmap(df_corr,annot = False)
	plt.show()	

##############################################################

def correlation_heatmap_of_log_values(list_of_stocks):

	df = pd.DataFrame()

	start_date = input("Enter start date : ")
	end_date = datetime.now() #input("Enter end date : ")

	for i in range(len(list_of_stocks)):
		data = yf.download(list_of_stocks[i], start_date,end_date)
		data = attach_log_column(data)
		# print(data.head(n = 3))
		# print("\n\n\n")

		log_column = data['Log_Column']
		df.insert(i,list_of_stocks[i],log_column)

	df_corr = df.corr()

	#print(df_corr.head(n = 5))

	df_corr.to_csv('df_corr.csv')

	df_corr_plot = sns.heatmap(df_corr,annot = False)
	plt.show()

###############################################################

def collect_data():

	data_frames = {}
	list_of_stocks = []

	n = int(input("Enter number of stocks : "))

	for i in range(n):
		list_of_stocks.append(input("Enter name of stock: "))

	start_date = input('Enter start date : ')
	end_date = datetime.now() #input("Enter end date : ")

	data = pd.read_csv("cnm_tsym.csv")
	symbol = data['Symbol'].tolist()
	company = data['Company'].tolist()

	for i in range(n):
		ticker_idx = company.index(list_of_stocks[i])
		name_data = yf.download(symbol[ticker_idx],start_date,end_date)
		data_frames[list_of_stocks[i]] = name_data

	for df in data_frames:

		print(data_frames[df].tail(n = 5))


###############################################################

option = 'y'

while(option == 'y'):

	print("1 : Look for stats : ")
	print("2 : Compare two stocks: ")
	print("3 : Correlation heat map of adjusted close values : ")
	print("4 : Correlation heat map of log values : ")
	print("5 : Collect data : ")

	choose = int(input("Enter your choice : "))

	if(choose == 1):
		stock_name = input("Enter stock name : ")
		Look_for_stats(stock_name)
	elif(choose == 2):
		first_stock = input("Enter name of first stock name : ")
		second_stock = input("Enter name of second stock name : ")

		Compare_2_stocks(first_stock,second_stock)

	elif(choose == 3):

		list_of_stocks = []
		no_of_stocks = int(input("Enter no. of stocks: "))

		for i in range(no_of_stocks):
			name = input("Enter name of stock: ")
			list_of_stocks.append(name)

		#list_of_stocks = ["TCS.NS","TATASTEEL.NS","TATAMOTORS.NS","TATAPOWER.NS","TITAN.NS","TATACHEM.NS","INDHOTEL.NS","ATACOMM.NS", "VOLTAS.NS", "TRENT.NS","TATASTLLP.NS", "TATAINVEST.NS", "TATAMETALI.NS", "TATAELXSI.NS", "NELCO.NS", "TATACOFFEE.NS" ]
		correlation_heatmap_of_adj_close(list_of_stocks)
	elif(choose == 4):

		list_of_stocks = ["TCS.NS","TATASTEEL.NS","TATAMOTORS.NS","TATAPOWER.NS","TITAN.NS","TATACHEM.NS","INDHOTEL.NS","TATACOMM.NS", "VOLTAS.NS", "TRENT.NS","TATASTLLP.NS", "TATAINVEST.NS", "TATAMETALI.NS", "TATAELXSI.NS", "NELCO.NS", "TATACOFFEE.NS" ]
		
		# list_of_stocks = []
		# no_of_stocks = int(input("Enter no. of stocks: "))

		# for i in range(no_onf_stocks):
		# 	name = input("Enter name of stock: ")
		# 	list_of_stocks.append(name)

		correlation_heatmap_of_adj_close(list_of_stocks)
		correlation_heatmap_of_log_values(list_of_stocks)

	else:

		collect_data()


	option = input("If you want to continue enter 'y' else 'n': ")
