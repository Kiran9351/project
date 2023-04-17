
import pandas as pd 
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta


def append_data(sym, e_date):

	data = pd.read_csv('append_data.csv')
	data = data.set_index('Date')
	data.index = pd.to_datetime(data.index, format = '%Y-%m-%d %H:%M:%S')

	
	no_of_rows = data.count()[sym]
	date = data.index[data.count()[sym]-1].date()
	
	rdf = data.iloc[no_of_rows:]
	data = data.iloc[:no_of_rows]
	

	start_date = date + timedelta(days = 1)
	# start_date = start_date.date()
	end_date = e_date

	df = yf.download(sym, start_date, end_date)
	rdf[sym] = pd.Series(df['Close'])

	data = pd.concat([data, rdf], axis = 0)
	# print(len(data[sym]))
	# print(data.count()['XOM'])

	data.to_csv('append_data.csv')


########################################################

def collect_data(list_of_stocks):

	data = pd.DataFrame()

	start_date = '2015-01-01'
	end_date = '2017-01-01'

	for sym in list_of_stocks:

		df = yf.download(sym, start_date, end_date)
		if(data.empty == True):
			data.index = df.index
			print(type(df.index[0]))

		data[sym] = pd.Series(df['Close'])


	data.to_csv('append_data.csv')

	return data

#######################################################

list_of_stocks = ['AAPL', 'AMZN', 'MRO', 'CVX', 'XOM']

data = collect_data(list_of_stocks)
# print(type(data.index[0]))
append_data('AAPL', '2018-01-01')
append_data('AMZN', '2018-01-01')
append_data('AMZN', '2019-01-01')
# append_data('MRO', '2018-01-01')
# append_data('CVX', '2018-01-01')

# date = data.index[0]
# date = date.to_pydatetime()
# print(type(date))
# print(date)