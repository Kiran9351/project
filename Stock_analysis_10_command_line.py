
# Implementing moving correlation in O(n)

import sys
import pandas as pd 
import math
import yfinance as yf
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

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

def moving_correlation_2(list_1, list_2, no_of_days):

	moving_cor = [None for i in range(no_of_days - 1)]

	x_sum = 0
	y_sum = 0
	xy = 0 
	x_sq_sum = 0 
	y_sq_sum = 0 

	x_sum = sum(list_1[:no_of_days - 1])
	y_sum = sum(list_2[:no_of_days - 1])
	xy = sum([(i*j) for i in list_1[:no_of_days] for j in list_2[:no_of_days]])
	x_sq_sum = sum([(i * i) for i in list_1[:no_of_days]])
	y_sq_sum = sum([(i * i) for i in list_2[:no_of_days]])
	x_mean = x_sum / (no_of_days - 1)
	y_mean = y_sum / (no_of_days - 1)

	for i in range(len(list_1[no_of_days-1:])):

		x_mean = (x_mean + list_1[i])/2
		y_mean = (y_mean + list_2[i])/2

		numerator = xy - (no_of_days * x_mean * y_mean)
		denominator = math.sqrt(x_sq_sum - (no_of_days * x_mean * x_mean)) * math.sqrt(y_sq_sum - (no_of_days * y_mean * y_mean))

		corr = numerator/denominator
		moving_cor.append(corr)

		x_sum = x_sum - list_1[i - (no_of_days - 1)]
		y_sum = y_sum - list_1[i - (no_of_days - 1)]
		xy = xy - (list_1[i - (no_of_days - 1)] * list_2[i - (no_of_days - 1)])
		x_sq_sum = x_sq_sum - (list_1[i - (no_of_days - 1)] * list_1[i - (no_of_days - 1)])
		y_sq_sum = y_sq_sum - (list_2[i - (no_of_days - 1)] * list_2[i - (no_of_days - 1)])


	return moving_cor




###############################################################

def Look_for_stats(stock_name,s_date, e_date = '', mdays = 21):

	start_date = s_date

	if(e_date != ''):
		end_date = e_date

	else:
		end_date = datetime.now()

	ticker = stock_name

	data = yf.download(ticker,start_date,end_date)

	data = attach_log_column(data)

	#################################################################################

	## To print mean, standard deviation, kurtosis
	
	close_mean = data['Close'].mean()
	standard_deviation_close = data['Close'].std()
	kurtosis_close = data['Close'].kurtosis()

	#################################################################################

	# Plotting close value graph.

	data['Close'].plot(figsize = (10,7),style = '-')

	plt.title('Close vs Year', fontsize = 16)
	plt.xlabel("Year",fontsize = 14)
	plt.ylabel("Close values",fontsize = 14)
	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)
	
	# plt.text(min(data['Close'].tolist()),max(data['Close'].tolist()), "mean = "+str(round(close_mean,3)))
	plt.text(0.5,0.04, 'Mean = '+str(round(close_mean,3)), ha = 'center', fontsize=11, color = 'red', transform=plt.gcf().transFigure)
	plt.text(0.5,0.02, ' Std_dev = '+str(round(standard_deviation_close,3)), ha = 'center', fontsize = 11, color = 'green', transform = plt.gcf().transFigure)
	plt.text(0.5,0.0, 'Kurtosis = '+str(round(kurtosis_close ,3)), ha = 'center', fontsize = 11, color = 'blue', transform = plt.gcf().transFigure)
	plt.legend()

	plt.show()		

	###############################################################################

	# Plotting returns graph.

	data['Log_Column'].plot(label = 'Return value points', figsize = (10,7), style = '.')

	plt.title('Return vs Year', fontsize = 16)
	plt.xlabel("Year",fontsize = 14)
	plt.ylabel("Return",fontsize = 14)
	plt.legend(edgecolor = 'red')

	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

	plt.show()

	###############################################################################
	
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

	# Moving average graph.

	#no_of_days = int(input("Enter number of days: "))
	moving_avg_hundred = moving_average(data,mdays)
	moving_avg_2_hundred = moving_average(data,2*mdays)


	plt.plot(data.index,moving_avg_hundred, label = str(mdays)+'_moving_avg')
	plt.plot(data.index,moving_avg_2_hundred, label = str(mdays*2)+'_moving_avg')
	data['Close'].plot(label = 'close', style = '-', figsize = (10,7))
	plt.title('Close and moving averages of ' + stock_name, fontsize = 16)
	plt.xlabel('Year',fontsize = 14)
	plt.ylabel('Moving avg',fontsize = 14)
	plt.legend()

	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
	plt.show()

##################################################################################################

def Compare_2_stocks(first_stock,second_stock,s_date, e_date = '', mdays = 21, cdays = 21):

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

	#################################################################################


	# Mean, standard deviation, kurtosis

	fmean_close = first_data['Close'].mean()
	fstandard_deviation_close = first_data['Close'].std()
	fkurtosis_close = first_data['Close'].kurtosis()

	smean_close = second_data['Close'].mean()
	sstandard_deviation_close = second_data['Close'].std()
	skurtosis_close = second_data['Close'].kurtosis()

	col = 'Log_Column' #input("Enter column name : ")
	corr = correlation_of_two_columns(first_data, second_data, col)

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

	plt.text(0.25, 0.07, first_stock, ha = 'center', fontsize = 13, color = 'blue', transform = plt.gcf().transFigure)
	plt.text(0.25,0.04, 'Mean = ' + str(round(fmean_close ,3)), ha = 'center', fontsize=11, color = 'red', transform=plt.gcf().transFigure)
	plt.text(0.25,0.02, 'Std_dev = ' + str(round(fstandard_deviation_close ,3)), ha = 'center', fontsize = 11, color = 'green', transform = plt.gcf().transFigure)
	plt.text(0.25,0.0, 'Kurtosis = ' + str(round(fkurtosis_close ,3)), ha  = 'center', fontsize = 11, color = 'blue', transform = plt.gcf().transFigure)

	plt.text(0.75, 0.07, second_stock, ha = 'center', fontsize = 13 , color = 'blue', transform = plt.gcf().transFigure)
	plt.text(0.75,0.04, 'Mean = ' + str(round(smean_close,3)), ha = 'center', fontsize=11, color = 'red', transform=plt.gcf().transFigure)
	plt.text(0.75,0.02, ' Std_dev = ' + str(round(sstandard_deviation_close,3)), ha = 'center', fontsize = 11, color = 'green', transform = plt.gcf().transFigure)
	plt.text(0.75,0.0, 'Kurtosis = ' + str(round(skurtosis_close ,3)), ha = 'center', fontsize = 11, color = 'blue', transform = plt.gcf().transFigure)

	plt.legend()

	plt.grid(which = 'major', linestyle ='-', linewidth = 0.5)

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
	
	plt.text(0.5,0.02, 'Correlation = ' + str(round(corr,6)), ha = 'center', color = 'red', fontsize = 12, transform = plt.gcf().transFigure)
	plt.legend()

	plt.show()
	

	#################################################################################

	# Moving averages of both data.

	#no_of_days = int(input("Enter number of days for moving averages : "))
	moving_avg_hundred = moving_average(first_data,mdays)
	moving_avg_2_hundred = moving_average(second_data,mdays)


	# plt.plot(first_data.index,moving_avg_hundred, label = str(mdays)+'_moving_avg_'+first_stock)
	# plt.plot(second_data.index,moving_avg_2_hundred, label = str(mdays)+'_moving_avg_'+second_stock)
	# first_data['Close'].plot(label = first_stock+'_close', style = '-', figsize = (10,7))
	# second_data['Close'].plot(label = second_stock+'_close', style = '-', figsize = (10,7))
	# plt.title('CLose values and Moving avg', fontsize = 15)
	# plt.xlabel('Year',fontsize = 14)
	# plt.ylabel('Moving avg',fontsize = 14)
	# plt.legend()

	# plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
	# plt.show()

	moving_avg_hundred = moving_average(first_data,mdays)
	moving_avg_2_hundred = moving_average(second_data,mdays)

	fig, axs = plt.subplots(2)
	fig.suptitle("Close and Moving Avg.")
	fig.set_figheight(10)
	fig.set_figwidth(12)

	axs[0].plot(first_data.index,moving_avg_hundred, label = str(mdays)+'_moving_avg_'+first_stock)
	axs[0].plot(first_data.index, first_data['Close'].tolist(), label = first_stock+'_close')
	axs[0].grid(which ='major', linestyle = '-.',linewidth = 0.5)
	axs[0].legend()

	axs[1].plot(second_data.index,moving_avg_2_hundred, label = str(mdays)+'_moving_avg_'+second_stock)
	axs[1].plot(first_data.index, second_data['Close'].tolist(), label = second_stock+'_close')
	axs[1].grid(which ='major', linestyle = '-.',linewidth = 0.5)
	#plt.title('CLose values and Moving avg', fontsize = 15)
	axs[1].legend()

	plt.show()

	#################################################################################

	# Moving correlation

	#cdays = int(input("Enter number of days for moving Correlation : "))
	moving_cor_1 = moving_correlation(first_data, second_data, 'Log_Column', cdays)
	moving_cor_2 = moving_correlation_2(first_data['Log_Column'].tolist(), second_data['Log_Column'].tolist(), cdays)

	# code to check equality of both functions.
	# if(moving_cor_2[cdays-1:].sort() == moving_cor_1[cdays - 1: ].sort()):
	# 	print("Both are equal")

	plt.figure(figsize = (10,7))
	plt.plot(first_data.index, moving_cor_1, label = str(cdays) + '_Moving_correlation')

	plt.xlabel('Year',fontsize = 14)
	plt.ylabel('Moving avg',fontsize = 14)
	plt.title(first_stock +' and ' + second_stock + ' Moving Corr', fontsize = 15)

	plt.legend()
	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)

	plt.show()

	#################################################################################

	x = first_data['Log_Column'].tolist()
	y = second_data['Log_Column'].tolist()

	x_mean = sum(x)/len(x)
	y_mean = sum(y)/len(y)
	numerator = 0
	denominator = 0

	for i in range(len(x)):
		numerator += ((x[i] - x_mean) * (y[i] - y_mean))
		denominator += ((x[i] - x_mean) * (x[i] -  x_mean))

	#slope
	SL = numerator/denominator
	#intercept
	IC = y_mean - (SL * x_mean)

	output = []

	for i in x:
		output.append((SL * i) + IC)

	plt.figure(figsize = (10,7))
	plt.scatter(x,y, label = 'Return_value_points')
	plt.plot(x,output, 'r', label = 'Linear_fit_line')
	plt.title('Linear fit of returns', fontsize = 15)
	plt.xlabel(first_stock, fontsize = 11)
	plt.ylabel(second_stock, fontsize = 11)
	plt.text(0.5,0.01, 'Intercept = ' + str(round(IC, 4)), ha = 'center', color = 'blue', fontsize = 12, transform = plt.gcf().transFigure)
	plt.text(0.5,0.03, 'Slope = ' + str(round(SL, 4)), ha = 'center', color = 'red', fontsize = 12, transform = plt.gcf().transFigure)
	plt.legend()
	plt.grid(which ='major', linestyle = '-.',linewidth = 0.5)
	plt.show()


###############################################################

def give_date(year, month, day):

	date = year + '-' + month + '-' + day
	date = datetime.strptime(date, '%Y-%m-%d')

	return date

###############################################################

def give_mdays(days):

	if(days % 10 == 0):
		mdays = int(days / 10)
	else:
		mdays = int((days - (days % 10) + 10)/10)
	print(mdays)

	return mdays

###############################################################

n = len(sys.argv)

#name ticker days 	3
if(n == 3):
	date = datetime.now() - timedelta(days = int(sys.argv[2]), hours = datetime.now().hour)
	mdays = give_mdays(int(sys.argv[2]))
	
	Look_for_stats(sys.argv[1], date, '', mdays)

#name ticker1 ticker2 days 	4
#name ticker days mdays 	4
elif(n == 4):

	if(sys.argv[2][:1] < 'A'):
		date = datetime.now() - timedelta(days = int(sys.argv[2]), hours = datetime.now().hour)
		
		Look_for_stats(sys.argv[1], date, '',int(sys.argv[3]))

	else:
		date = datetime.now() - timedelta(days = int(sys.argv[3]), hours = datetime.now().hour)

		mdays = give_mdays(int(sys.argv[2]))
		
		Compare_2_stocks(sys.argv[1],sys.argv[2],date, '', mdays, mdays)

#name ticker1 year month day 	5
#name ticker1 ticker2 days mdays	5 
elif(n == 5):

	if(sys.argv[2][:1] < 'A'):
		s_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])
		
		days = (datetime.now().date() - s_date.date()).days
		mdays = give_mdays(days)
		
		Look_for_stats(sys.argv[1], s_date, '', mdays)

	else:
		s_date = datetime.now() - timedelta(days = int(sys.argv[3]), hours = datetime.now().hour)
		
		Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, datetime.now(), int(sys.argv[4]))


elif(n == 6):

	if(sys.argv[2][:1] < 'A'):

		#name ticker1 year month day mdays 	6	-d
		if(int(sys.argv[5]) <= 100):
			s_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])
		
			Look_for_stats(sys.argv[1], s_date, datetime.now(), int(sys.argv[5]))

		# name ticker year month day days 	6	- d	
		else:
			s_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])
			e_date = s_date + timedelta(days = int(sys.argv[5]))

			mdays = give_mdays(int(sys.argv[5]))

			Look_for_stats(sys.argv[1], s_date, e_date)

	else:
		#name ticker1 ticker2 year month day 	6	- d
		if(int(sys.argv[4]) <= 12):
			s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])

			days = (datetime.now().date() - s_date.date()).days
			mdays = give_mdays(days)
		
			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, '', mdays, mdays)

		#name ticker1 ticker2 days mdays cdays	6	- d
		else:
			s_date = datetime.now() - timedelta(days = int(sys.argv[3]), hours = datetime.now().hour)
		
			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, '', int(sys.argv[4]), int(sys.argv[5]))

elif(n == 7):

	if(sys.argv[2][:1] < 'A'):
		# name ticker year month day days mdays		7	-d
		s_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])
		e_date = s_date + timedelta(days = int(sys.argv[5]))

		Look_for_stats(sys.argv[1], s_date, e_date, int(sys.argv[6]))

	else:

		if(int(sys.argv[6]) <= 100):
			#name ticker1 ticker2 year month day mdays 7	- d
			s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])

			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, '', int(sys.argv[6]))

		else:
			# name ticker1 ticker2 year month day days 7	- d
			s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])
			e_date = s_date + timedelta(days = int(sys.argv[6]))

			mdays = give_mdays(int(sys.argv[6]))

			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, e_date, mdays, mdays)


elif(n == 8):

	if(sys.argv[2][:1] < 'A'):
		# name ticker year month day  year month day 	8	-d
		s_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])
		e_date = give_date(sys.argv[5], sys.argv[6], sys.argv[7])

		days = (e_date.date() - s_date.date()).days
		mdays = give_mdays(days)

		Look_for_stats(sys.argv[1], s_date, e_date, mdays, mdays)

	else:
		#name ticker1 ticker2 year month day mdays cdays	8 	-d
		if(int(sys.argv[6]) <= 100):
			s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])

			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, '', int(sys.argv[6]), int(sys.argv[7]))

		# name ticker1 ticker2 year month day days mdays 8	-d
		else:

			s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])
			e_date = s_date + timedelta(days = int(sys.argv[6]))

			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, e_date, int(sys.argv[7]))

elif(n == 9):

	# name ticker year month day  year month day mdays	9	-d
	if(sys.argv[2][:1] < 'A'):

		s_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])
		e_date = give_date(sys.argv[5], sys.argv[6], sys.argv[7])

		Look_for_stats(sys.argv[1], s_date, e_date, int(sys.argv[8]))

	else:
		# name ticker1 ticker2 year month day year month day 	9 -d
		if(int(sys.argv[7]) <= 12):

			s_date = give_date(sys.argv[3],sys.argv[4], sys.argv[5])
			e_date = give_date(sys.argv[6], sys.argv[7], sys.argv[8])

			days = (e_date.date() - s_date.date()).days
			mdays = give_mdays(days)

			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, e_date, mdays, mdays)

		else:
			# name ticker1 ticker2 year month day days mdays cdays 9	-d
			s_date = give_date(sys.argv[3],sys.argv[4], sys.argv[5])
			e_date = s_date + timedelta(days = int(sys.argv[6]))

			Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, e_date, int(sys.argv[7]),int(sys.argv[8]))


# name ticker1 ticker2 year month day year month day mdays	10
elif(n == 10):

	s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])
	e_date = give_date(sys.argv[6], sys.argv[7], sys.argv[8])
	Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, e_date, int(sys.argv[9]))

# name ticker1 ticker2 year month day year month day mdays cdays 11
elif(n == 11):

	s_date = give_date(sys.argv[3], sys.argv[4], sys.argv[5])
	e_date = give_date(sys.argv[6], sys.argv[7], sys.argv[8])
	Compare_2_stocks(sys.argv[1], sys.argv[2], s_date, e_date, int(sys.argv[9]), int(sys.argv[10]))


else:

	print("In this program we have two Funtions: ")
	print("1 : Look_for_stats()\n2 : Compare_2_stocks()")
	print("\nFunction Description:")
	print("\nStart and end date format = yyyy mm dd")
	print("no_of_days_before_today and no_of_days_after_start_date are assumed to be more than 100 days\n")
	print("1: Look_for_stats(stock_symbol, start_date, end_date, moving_average_days)")
	print("""\nDefault Values for this funtion:\n
		stock_symbol = [No Default Value]\n
		start_date = [No Default Value]\n
		end_date = [todays date]\n
		moving_average_days = [30]\n
		""")
	
	print("\nNo. of ways you can give parameters to Function:")
	print("""\n
		1) program_name stock_symbol no_of_days_before_today\n
		2) program_name stock_symbol no_of_days_before_today moving_average_days\n
		3) program_name stock_symbol start_date\n
		4) program_name stock_symbol start_date moving_average_days\n
		5) program_name stock_symbol start_date no_of_days_after_start_sate\n
		6) program_name stock_symbol start_date no_of_days_aafter_start_date moving_avg_days\n
		7) program_name stock_symbol start_date end_date\n
		8) program_name stock_symbol start_date end_date moving_avg_days\n
		""")
	print("2 : Compare_2_stocks(stock_symbol_1, stock_symbol_2, start_date, end_date, moving_average_days, moving_correlation_days)")
	print("""\nDefault Values for this function:\n
		stock_symbol_1 = [No Default Value]\n
		stock_symbol_2 = [No Default Value]\n
		start_date = [No Default Value]\n
		end_date = [todays date]\n
		moving_average_days = [30]\n
		moving_correlation_days = [30]\n
		""")
	print("\nNo. of ways you can give parameters to function : ")
	print("""\n
		1) program_name stock_symbol_1 stock_symbol_2 no_of_days_before_today\n
		2) program_name stock_symbol_1 stock_symbol_2 no_of_days_before_today moving_average_days\n
		3) program_name stock_symbol_1 stock_symbol_2 start_date\n
		4) program_name stock_symbol_1 stock_symbol_2 no_of_days_before_today moving_average_days moving_correlation_days\n
		5) program_name stock_symbol_1 stock_symbol_2 start_date moving_average_days\n
		6) program_name stock_symbol_1 stock_symbol_2 start_date no_of_days_after_start_date\n
		7) program_name stock_symbol_1 stock_symbol_2 start_date moving_average_days moving_correlation_days\n
		8) program_name stock_symbol_1 stock_symbol_2 start_date no_of_days_after_start_date moving_average_days\n
		9) program_name stock_symbol_1 stock_symbol_2 start_date end_date\n
		10) program_name stock_symbol_1 stock_symbol_2 start_date no_of_days_after_start_date moving_average_days moving_correlation_days\n
		11) program_name stock_symbol_1 stock_symbol_2 start_date end_date moving_average_days\n
		12) program_name stock_symbol_1 stock_symbol_2 start_date end_date moving_average_days moving_correlation_days\n
		""")
