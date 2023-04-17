
import sys
import pandas as pd 
import math
import yfinance as yf
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

def Look_for_stats(stock_name,s_date, e_date = '', mdays = 50):

	start_date = s_date

	if(e_date != ''):
		end_date = e_date

	else:
		end_date = datetime.now()

	ticker = stock_name

	data = yf.download(ticker,start_date,end_date)

	#print(type(data))

	data = attach_log_column(data)

	print("Printing last 5 rows of data:\n\n")
	print(data.head(n = 5))
	print("\n\n\n")

	#################################################################################

	## To print mean, standard deviation, kurtosis
	
	close_mean = data['Close'].mean()
	standard_deviation_close = data['Close'].std()
	kurtosis_close = data['Close'].kurtosis()

	print("\nMean of close values : ",round(close_mean, 3))
	print("standard deviation of close values : ",round(standard_deviation_close, 3))
	print("Kurtosis of close values : ",round(kurtosis_close, 3))
	print('\n\n')

	#################################################################################

	# Frequency distribution of returns

	log_list = data['Log_Column'].tolist()
	min_num = min(log_list)
	max_num = max(log_list)
	no_bins = round(max_num + (min_num * (-1)))

	plt.hist(log_list, bins = no_bins, label = stock_name)

	plt.title("Frequencies vs Return values", fontsize = 16)
	plt.xlabel('Returns', fontsize = 14)
	plt.ylabel('Frequencies', fontsize = 14)
	plt.legend()

	plt.show()

	###############################################################################

	# Plotting returns graph.

	data['Log_Column'].plot(figsize = (10,7), style = '.')

	plt.title('Return vs Year', fontsize = 16)
	plt.xlabel("Year",fontsize = 14)
	plt.ylabel("Return",fontsize = 14)

	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

	plt.show()

	###############################################################################
	
	# Plotting close value graph.

	data['Close'].plot(figsize = (10,7),style = '-')

	plt.title('Close vs Year', fontsize = 16)
	plt.xlabel("Year",fontsize = 14)
	plt.ylabel("Close values",fontsize = 14)
	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

	plt.show()			

	###############################################################################

	# Moving average graph.

	#no_of_days = int(input("Enter number of days: "))
	moving_avg_hundred = moving_average(data,mdays)
	moving_avg_2_hundred = moving_average(data,2*mdays)


	plt.plot(data.index,moving_avg_hundred, label = str(no_of_days)+'_moving_avg')
	plt.plot(data.index,moving_avg_2_hundred, label = str(no_of_days*2)+'_moving_avg')
	data['Close'].plot(label = 'close', style = '-', figsize = (10,7))
	plt.title('Close and moving averages of ' + stock_name, fontsize = 16)
	plt.xlabel('Year',fontsize = 14)
	plt.ylabel('Moving avg',fontsize = 14)
	plt.legend()

	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
	plt.show()

##################################################################################################

def Compare_2_stocks(first_stock,second_stock,s_date, e_date = '', mdays = 50, cdays = 30):

	start_date = s_date

	if(e_date != ''):
		end_date = e_date

	else:
		end_date = datetime.now()

	ticker1 = first_stock
	first_data = yf.download(ticker1,start_date,end_date)
	
	ticker2 = second_stock
	second_data = yf.download(ticker2,start_date,end_date)

	first_data = attach_log_column(first_data)
	second_data = attach_log_column(second_data)

	# print("Last few rows of first stock data :\n\n")
	# print(first_data.head(n = 5))
	# print("\n\n\n")

	# print("Last few row of second stock data : \n\n")
	# print(second_data.head(n = 5))
	# print("\n")

	#################################################################################


	# Mean, standard deviation, kurtosis

	fmean_close = first_data['Close'].mean()
	fstandard_deviation_close = first_data['Close'].std()
	fkurtosis_close = first_data['Close'].kurtosis()

	print("\nMean of close values of ", first_stock, ' : ', round(fmean_close,3))
	print("standard deviation of close values of ",first_stock, ' : ', round(fstandard_deviation_close, 3))
	print("Kurtosis of close values of ", first_stock, ' : ', round(fkurtosis_close, 3))
	print("\n")

	smean_close = second_data['Close'].mean()
	sstandard_deviation_close = second_data['Close'].std()
	skurtosis_close = second_data['Close'].kurtosis()

	print("Mean of close values of ", second_stock, ' : ', round(smean_close, 3))
	print("standard deviation of close values of ", second_stock , ' : ', round(sstandard_deviation_close, 3))
	print("Kurtosis of close values of ", second_stock, ' : ',round(skurtosis_close, 3))
	col = 'Log_Column' #input("Enter column name : ")
	corr = correlation_of_two_columns(first_data, second_data, col)
	print('Correlation = ',round(corr, 3))
	print("\n")

	#################################################################################

	# Frequency distribution of return values.
	
	log_list_1 = first_data['Log_Column'].tolist()
	log_list_2 = second_data['Log_Column'].tolist()

	min_num = min(log_list_1)
	max_num = max(log_list_1)
	no_bins = round(max_num + (min_num * (-1)))

	plt.figure(figsize = (10,7))
	plt.hist([log_list_1, log_list_2], bins = no_bins, label = [first_stock, second_stock])
	
	plt.title('Frequencies vs Return values', fontsize = 16)
	plt.xlabel('Returns', fontsize = 14)
	plt.ylabel('Frequencies', fontsize = 14)
	plt.legend()

	plt.show()

	#################################################################################
		
	# Graph of return values

	first_data['Log_Column'].plot(figsize = (10,7), style = '.', label = first_stock)
	second_data['Log_Column'].plot(figsize = (10,7), style = '.', label = second_stock)
	plt.title('Return vs Year', fontsize = 16)
	plt.xlabel("Year",fontsize = 14)
	plt.ylabel("Return",fontsize = 14)
	plt.legend()

	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

	plt.show()

	#################################################################################
		
	# Graph of close values and spread values.

	first_data['Close'].plot(label = first_stock, figsize = (10,7),style = '-')
	second_data['Close'].plot(label = second_stock, figsize = (10,7), style = '-')

	spread = []

	if(abs(first_data['Close'].mean() - second_data['Close'].mean()) > 200):

		if(first_data['Close'].mean() > second_data['Close'].mean()):
			scale = (first_data['Close'].mean()/second_data['Close'].mean()) - 1
			scale = round(scale)

			for i in range(len(first_data['Close'])):
				spread.append(abs(first_data['Close'][i] - (second_data['Close'][i] * scale)))

		else:
			scale = (second_data['Close'].mean()/first_data['Close'].mean()) - 1
			scale = round(scale)

			for i in range(len(first_data['Close'])):
				spread.append(abs(second_data['Close'][i] - (first_data['Close'][i] * scale)))

	else:
		scale = 1

		for i in range(len(first_data['Close'])):
				spread.append(abs(second_data['Close'][i] - (first_data['Close'][i] * scale)))

	

	plt.plot(first_data.index, spread, label = 'Spread x '+str(scale), linestyle = '-')
	plt.title('[Close, Spread] vs Year', fontsize = 16)
	plt.xlabel("Year",fontsize = 14)
	plt.ylabel("Close values",fontsize = 14)
	plt.legend()

	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

	plt.show()

	#################################################################################

	# Moving averages of both data.

	#no_of_days = int(input("Enter number of days for moving averages : "))
	moving_avg_hundred = moving_average(first_data,mdays)
	moving_avg_2_hundred = moving_average(second_data,mdays)


	plt.plot(first_data.index,moving_avg_hundred, label = str(no_of_days)+'_moving_avg_'+first_stock)
	plt.plot(second_data.index,moving_avg_2_hundred, label = str(no_of_days)+'_moving_avg_'+second_stock)
	first_data['Close'].plot(label = first_stock+'_close', style = '-', figsize = (10,7))
	second_data['Close'].plot(label = second_stock+'_close', style = '-', figsize = (10,7))
	plt.xlabel('Year',fontsize = 14)
	plt.ylabel('Moving avg',fontsize = 14)
	plt.legend()

	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
	plt.show()

	#################################################################################

	# Moving correlation

	#cdays = int(input("Enter number of days for moving Correlation : "))
	moving_cor = moving_correlation(first_data, second_data, 'Log_Column', cdays)

	plt.figure(figsize = (10,7))
	plt.plot(first_data.index, moving_cor, label = 'Moving_correlation')

	plt.xlabel('Year',fontsize = 14)
	plt.ylabel('Moving avg',fontsize = 14)

	plt.legend()
	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)

	plt.show()

	#################################################################################

	# linear fit.
	x = first_data['Log_Column'].values.reshape(-1,1)
	y = second_data['Log_Column'].values.reshape(-1,1)

	linear_regessor = LinearRegression() 
	
	linear_regessor.fit(x, y)
	Y_pred = linear_regessor.predict(x)

	plt.figure(figsize = (10,7))
	plt.scatter(x,y)
	plt.plot(x,Y_pred,color = 'red')
	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)


	plt.show()


###############################################################

n = len(sys.argv)

#name ticker days
if(n == 3):
	ticker = sys.argv[1]
	no_of_days = int(sys.argv[2])

	#print("ticker is : ",ticker)
	#print("Days : ",no_of_days)

	date = datetime.now() - timedelta(days = no_of_days, hours = datetime.now().hour)
	#print(type(date))
	#print(date)

	Look_for_stats(ticker,date)

#name ticker1 ticker2 days
elif(n == 4):
	ticker1 = sys.argv[1]
	ticker2 = sys.argv[2]
	no_of_days = int(sys.argv[3])

	# print("First stock is : ",ticker1)
	# print("Second stock is : ",ticker2)
	# print("Days : ",no_of_days)

	date = datetime.now() - timedelta(days = no_of_days, hours = datetime.now().hour)
	# print(date)

	Compare_2_stocks(ticker1,ticker2,date)

#name ticker1 year month day
elif(n == 5):
	ticker = sys.argv[1]
	date = sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[4]
	date = datetime.strptime(date, '%Y-%m-%d')

	# print("Stock name is : ", ticker)
	# print("Date : ",date)

	Look_for_stats(ticker,date)

#name ticker1 ticker2 year month day
# name ticker year month day days
elif(n == 6):

	if(int(sys.argv[3]) > 1000):
		ticker1 = sys.argv[1]      
		ticker2 = sys.argv[2]
		date = sys.argv[3] + '-' + sys.argv[4] + '-' + sys.argv[5]
		date = datetime.strptime(date,'%Y-%m-%d')

		# print("First stock is : ",ticker1)
		# print("Second stock is : ",ticker2)
		# print("Date : ",date)

		Compare_2_stocks(ticker1,ticker2,date)

	else:
		ticker = sys.argv[1]      
		s_date = sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[4]
		s_date = datetime.strptime(s_date,'%Y-%m-%d')

		e_date = s_date + timedelta(days = int(sys.argv[5]))
		# print("First stock is : ",ticker1)
		# print("Second stock is : ",ticker2)
		# print("Date : ",date)

		Look_for_stats(ticker,s_date,e_date)

# name ticker1 ticker2 year month day days
elif( n == 7):
	ticker1 = sys.argv[1]      
	ticker2 = sys.argv[2]
	s_date = sys.argv[3] + '-' + sys.argv[4] + '-' + sys.argv[5]
	s_date = datetime.strptime(s_date,'%Y-%m-%d')

	e_date = s_date + timedelta(days = int(sys.argv[6]))

	Compare_2_stocks(ticker1,ticker2,s_date,e_date)

# name ticker year month day  year month day
elif(n == 8):
	ticker = sys.argv[1]
	s_date = sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[4]
	s_date = datetime.strptime(s_date,'%Y-%m-%d')
	e_date = sys.argv[5] + '-' + sys.argv[6] + '-' + sys.argv[7]
	e_date = datetime.strptime(e_date,'%Y-%m-%d')

	Look_for_stats(ticker1,ticker2,s_date,e_date)

# name ticker1 ticker2 year month day year month day
elif(n == 9):

	ticker1 = sys.argv[1]      
	ticker2 = sys.argv[2]
	s_date = sys.argv[3] + '-' + sys.argv[4] + '-' + sys.argv[5]
	s_date = datetime.strptime(s_date,'%Y-%m-%d')
	e_date = sys.argv[6] + '-' + sys.argv[7] + '-' + sys.argv[8]
	e_date = datetime.strptime(e_date,'%Y-%m-%d')

	Compare_2_stocks(ticker1,ticker2,s_date,e_date)



