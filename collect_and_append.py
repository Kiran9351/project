
import pandas as pd 
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import math
import sys

##################################################################

def attach_log_column(data):
	log_column = [0]
	#adj_column = data['Adj Close'].tolist()
	adj_column = data['Close'].tolist()
	#print(adj_column)

	for i in range(1,len(adj_column)):
		div_val = adj_column[i]/adj_column[i-1]
		log_column.append(math.log(div_val))

	data = data.assign(Log_Column=log_column)
	#data.head()

	return data

#################################################################

def collect_data(tickers, s_date, e_date):
	close_data = pd.DataFrame()
	log_data = pd.DataFrame()
	cdata = pd.DataFrame()
	ldata = pd.DataFrame()

	start_date = s_date
	end_date = e_date

	i = 0
	df= pd.DataFrame()

	df1 = yf.download(tickers[0], start_date, end_date)
	df1 = attach_log_column(df1)
	#df1 = df1[::-1]
	close_data.index = df1.index[::-1]
	log_data.index = df1.index[::-1]
	close_data[tickers[0]] = pd.Series(df1['Close'][::-1])
	log_data['Log_'+tickers[0]]= pd.Series(df1['Log_Column'][::-1])

	cdata.index = df1.index[::-1]
	ldata.index = df1.index[::-1]

	for sym in tickers[1:]:
		df = yf.download(sym , start_date, end_date)

		if(df.empty == False):
			df = attach_log_column(df)
			#df = df[::-1]
			cdata[sym] = pd.Series(df['Close'][::-1])
			ldata['Log_'+sym] = pd.Series(df['Log_Column'][::-1])
			i += 1

		if(i == 100):
			close_data = pd.concat([close_data, cdata], axis = 1)
			log_data= pd.concat([log_data, ldata], axis = 1)
			cdata = pd.DataFrame()
			ldata = pd.DataFrame()
			cdata.index = df1.index[::-1]
			ldata.index = df1.index[::-1]
			i = 0

	if(cdata.empty == False):
		close_data = pd.concat([close_data, cdata], axis = 1)
		log_data= pd.concat([log_data, ldata], axis = 1)


	return close_data, log_data

################################################################

def give_date(year, month, day):

	date = year + '-' + month + '-' + day
	date = datetime.strptime(date, '%Y-%m-%d')

	return date

################################################################

company_data = pd.read_csv('Company_names.csv')
tickers = company_data['Symbol'].tolist()

n = len(sys.argv)

if(n > 1):
	if(sys.argv[1].upper() == '-C'):

		s_date = give_date(sys.argv[2],sys.argv[3],sys.argv[4])
		e_date = give_date(sys.argv[5],sys.argv[6],sys.argv[7])

		close_data, log_data = collect_data(tickers, s_date, e_date)
		
		close_data.to_csv('close_data.csv')
		log_data.to_csv('log_data.csv')
	else:

		data = pd.read_csv('close_data.csv')
		ldata = pd.read_csv('log_data.csv')
		data = data.set_index('Date')
		ldata = ldata.set_index('Date')

		# new change = format
		data.index = pd.to_datetime(data.index, format = '%Y-%m-%d %H:%M:%S')
		ldata.index = pd.to_datetime(ldata.index, format = '%Y-%m-%d %H:%M:%S')

		s_date = data.index.tolist()[0]

		if(s_date.date() == (datetime.now()-timedelta(days = 1)).date()):
			print("Data is already updated")
		else:

			if(n == 2):
				e_date = datetime.now()
			else:
				e_date = give_date(sys.argv[2], sys.argv[3], sys.argv[4])

			close_data, log_data = collect_data(tickers, s_date, e_date)

			data = data.drop(s_date)
			log_data = log_data.drop(s_date)
			close_data = pd.concat([close_data, data], axis = 0)
			log_data = pd.concat([log_data, ldata], axis = 0)

			close_data.to_csv('close_data.csv')
			log_data.to_csv('log_data.csv')

else:

	print("This code is to collect and append data of 'close' values and 'log' values")
	
	print("\nCommand to collect data:")
	print("python [Program_name] [-C/-c] [start_date] [end_date]")
	print('start and end date form : year month day')
	print("\nWhile collecting data for first time it will create two '.csv' files:\nclose_data.csv - To keep close values\nlog_data.csv - To keep log values")
	print("\nCommand to append data till to today:")
	print("python [Program_name] [-A/-a]")

################################################################