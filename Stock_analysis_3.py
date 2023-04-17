import pandas as pd 
import math
import yfinance as yf
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import seaborn as sns

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

def moving_average(data,no_of_days): 

	moving_avg = [None for i in range(no_of_days - 1)]
	total = 0

	for i in range(len(data)):
		total = total + data['Close'][i]
		if(i >= (no_of_days - 1)):
			avg = total/no_of_days
			total = total - data['Close'][i - (no_of_days - 1)]
			moving_avg.append(avg)

	return moving_avg

###############################################################

def correlation_of_two_columns(first_data,second_data, col):

	list_1 = first_data[col].tolist()
	list_2 = second_data[col].tolist()

	m_1 = sum(list_1)/len(list_1)
	m_2 = sum(list_2)/len(list_2)

	numerator = 0
	denom_1 = 0
	denom_2 = 0

	for i in range(len(list_1)):
		numerator += ((list_1[i] - m_1) * (list_2[i] - m_2))
		denom_1 += ((list_1[i] - m_1) * (list_1[i] - m_1))
		denom_2 += ((list_2[i] - m_2) * (list_2[i] - m_2))
		

	denominator = math.sqrt(denom_1) * math.sqrt(denom_2)

	corr = numerator/denominator

	return corr


###############################################################

def moving_correlation(first_data, second_data, col,no_of_days):
	list_1 = first_data[col].tolist()
	list_2 = second_data[col].tolist()

	moving_cor = [None for i in range(no_of_days - 1)]

	m_1 = 0
	m_2 = 0
	s1 = 0
	s2 = 0

	numerator = 0
	denom_1 = 0
	denom_2 = 0
	denominator = 0
	k = 0

	for i in range(len(list_1)):
		s1 += list_1[i]
		s2 += list_2[i]

		if(i >= (no_of_days - 1)):
			m_1 = s1/no_of_days
			m_2 = s2/no_of_days

			for j in range(k,(k + no_of_days)):
				numerator += ((list_1[j] - m_1) * (list_2[j] - m_2))
				denom_1 += ((list_1[j] - m_1) * (list_1[j] - m_1))
				denom_2 += ((list_2[j] - m_2) * (list_2[j] - m_2))


			denominator = math.sqrt(denom_1) * math.sqrt(denom_2)

			corr = numerator/denominator
			moving_cor.append(corr)

			s1 = s1 - list_1[i - (no_of_days - 1)]
			s2 = s2 - list_2[i - (no_of_days - 1)]
			k += 1
			numerator = 0
			denom_1 = 0
			denom_2 = 0


	return moving_cor


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
		print("1 : To get mean, standard deviation, kurtosis")
		print("2 : Frequency distribution of return values")
		print("3 : Graph of return values")
		print("4 : Graph of closing values")
		print("5 : Moving averages")

		choose = int(input("Choose the option above: "))

		if(choose == 1):

			close_mean = data['Close'].mean()
			standard_deviation_close = data['Close'].std()
			kurtosis_close = data['Close'].kurtosis()

			print("Mean of close values : ",close_mean)
			print("standard deviation of close values : ",standard_deviation_close)
			print("Kurtosis of close values : ",kurtosis_close)

		elif(choose == 2):

			log_list = data['Log_Column'].tolist()
			min_num = min(log_list)
			max_num = max(log_list)
			no_bins = round(max_num + (min_num * (-1)))

			plt.hist(log_list, bins = no_bins)
			plt.show()

			

		elif(choose == 3):

			data['Log_Column'].plot(figsize = (10,7), style = '.')

			plt.title('Return vs Year', fontsize = 16)
			plt.xlabel("Year",fontsize = 14)
			plt.ylabel("Return",fontsize = 14)

			plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

			plt.show()

		elif(choose == 4):
			data['Close'].plot(figsize = (10,7),style = '.')

			plt.title('Close vs Year', fontsize = 16)
			plt.xlabel("Year",fontsize = 14)
			plt.ylabel("Close values",fontsize = 14)
			plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

			plt.show()

		elif(choose == 5):
			no_of_days = int(input("Enter number of days: "))
			moving_avg_hundred = moving_average(data,no_of_days)
			moving_avg_2_hundred = moving_average(data,2 * no_of_days)


			plt.plot(data.index,moving_avg_hundred, label = str(no_of_days)+'_moving_avg')
			plt.plot(data.index,moving_avg_2_hundred, label = str(no_of_days * 2)+'_moving_avg')
			data['Close'].plot(label = 'close', style = '-', figsize = (10,7))
			plt.xlabel('Year',fontsize = 14)
			plt.ylabel('Moving avg',fontsize = 14)
			plt.legend()

			plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
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

		print("1 : mean, standard deviation, kurtosis")
		print("2 : Frequency distribution of return values")
		print("3 : Graph of return values")
		print("4 : Graph of closing values")
		print("5 : Moving averages")
		print("6 : Correlation")
		print("7 : Linear fit curve with slope value")
		print("8 : Moving Correlation")

		choose = int(input("Enter your option : "))

		if(choose == 1):
			fmean_close = first_data['Close'].mean()
			fstandard_deviation_close = first_data['Close'].std()
			fkurtosis_close = first_data['Close'].kurtosis()

			print("Mean of close values of : ",first_stock,fmean_close)
			print("standard deviation of close values of : ",first_stock,fstandard_deviation_close)
			print("Kurtosis of close values of : ",first_stock,fkurtosis_close)
			print("\n\n")

			smean_close = second_data['Close'].mean()
			sstandard_deviation_close = second_data['Close'].std()
			skurtosis_close = second_data['Close'].kurtosis()

			print("Mean of close values of : ",second_stock,smean_close)
			print("standard deviation of close values of : ",second_stock,sstandard_deviation_close)
			print("Kurtosis of close values of : ",second_stock,skurtosis_close)


		elif(choose == 2):
			log_list_1 = first_data['Log_Column'].tolist()
			log_list_2 = second_data['Log_Column'].tolist()

			min_num = min(log_list_1)
			max_num = max(log_list_1)
			no_bins = round(max_num + (min_num * (-1)))

			plt.hist([log_list_1, log_list_2], bins = no_bins, label = [first_stock, second_stock])

			plt.legend()

			plt.show()

		elif(choose == 3):
			first_data['Log_Column'].plot(figsize = (10,7), style = '.', label = first_stock)
			second_data['Log_Column'].plot(figsize = (10,7), style = '.', label = second_stock)
			plt.title('Return vs Year', fontsize = 16)
			plt.xlabel("Year",fontsize = 14)
			plt.ylabel("Return",fontsize = 14)
			plt.legend()

			plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

			plt.show()

		elif(choose == 4):
			first_data['Close'].plot(label = first_stock, figsize = (10,7),style = '-')
			second_data['Close'].plot(label = second_stock, figsize = (10,7), style = '-')

			plt.title('Close vs Year', fontsize = 16)
			plt.xlabel("Year",fontsize = 14)
			plt.ylabel("Close values",fontsize = 14)
			plt.legend()

			plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

			plt.show()

		elif(choose == 5):
			no_of_days = int(input("Enter number of days: "))
			moving_avg_hundred = moving_average(first_data,no_of_days)
			moving_avg_2_hundred = moving_average(second_data,no_of_days)


			plt.plot(first_data.index,moving_avg_hundred, label = '100_moving_avg_'+first_stock)
			plt.plot(second_data.index,moving_avg_2_hundred, label = '100_moving_avg_'+second_stock)
			first_data['Close'].plot(label = first_stock+'_close', style = '-', figsize = (10,7))
			second_data['Close'].plot(label = second_stock+'_close', style = '-', figsize = (10,7))
			plt.xlabel('Year',fontsize = 14)
			plt.ylabel('Moving avg',fontsize = 14)
			plt.legend()

			plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
			plt.show()

		elif(choose == 6):
			col = input("Enter column name : ")
			corr = correlation_of_two_columns(first_data, second_data, col)
			print(corr)

		elif(choose == 7):

			x = first_data['Close'].values.reshape(-1,1)
			y = second_data['Close'].values.reshape(-1,1)

			linear_regessor = LinearRegression() 
			
			linear_regessor.fit(x, y)
			Y_pred = linear_regessor.predict(x)

			plt.scatter(x,y)
			plt.plot(x,Y_pred,color = 'red')

			plt.show()
			

		elif(choose == 8):

			col = input("Enter name of column : ")
			days = int(input("Enter number of days: "))
			moving_cor = moving_correlation(first_data, second_data, col, days)

			plt.plot(first_data.index, moving_cor, label = 'Moving_correlation')

			plt.xlabel('Year',fontsize = 14)
			plt.ylabel('Moving avg',fontsize = 14)

			plt.legend()
			plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)

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

	choose = int(input("Enter your choice : "))

	if(choose == 1):
		stock_name = input("Enter stock name : ")
		Look_for_stats(stock_name)
	elif(choose == 2):
		first_stock = input("Enter name of first stock name : ")
		second_stock = input("Enter name of second stock name : ")

		Compare_2_stocks(first_stock,second_stock)


	option = input("If you want to continue enter 'y' else 'n': ")