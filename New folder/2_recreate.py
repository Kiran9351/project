

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import statistics


def create_log_column(close_values):

	list_ = []

	for i in range(len(close_values) - 1):
		div = close_values[i]/close_values[i+1]
		list_.append(round(math.log(div),8))

	list_.append(0)

	return list_

##########################################################

def create_xom_cvx_data(close_data, log_data, close_log_data):

	xom_cvx_data = pd.DataFrame()

	xom_cvx_data['XOM'] = close_data['XOM']
	xom_cvx_data['CVX'] = close_data['CVX']

	spread = []
	ratio = []

	for i in range(len(close_data['XOM'])):
		spread.append(round(close_data['CVX'][i] - close_data['XOM'][i], 2))
		ratio.append(round(close_data['CVX'][i]/close_data['XOM'][i],9))

	xom_cvx_data['Spread'] = spread
	xom_cvx_data['Ratio'] = ratio

	xom_cvx_data['Log_XOM'] = log_data['XOM']
	xom_cvx_data['Log_CVX'] = log_data['CVX']

	xom_cvx_data.index = close_data.index
	xom_cvx_data.to_csv('xom_cvx.csv')

	combined_data = pd.concat([close_log_data, xom_cvx_data], axis = 1)
	combined_data.to_csv('combined_data.csv')

	return xom_cvx_data, combined_data


##########################################################

def log_columns(close_data):

	log_data = pd.DataFrame()
	list_ = []

	for col in close_data:
		close_values = close_data[col].values
		list_ = create_log_column(close_values)
		log_data[col] = list_
		# list_ = []
		# for i in range(len(close_values) - 1):
		# 	div = close_values[i]/close_values[i+1]
		# 	list_.append(math.log(div))

	log_data.index = close_data.index
	close_log_data = pd.concat([close_data,log_data],axis = 1)
	#close_data.to_csv('Energy_close_log.csv')
	log_data.to_csv('returns.csv')

	return log_data, close_log_data

##############################################################

def top_corr(df_corr):

	# print(df_corr.columns)

	clen = len(df_corr.columns)
	
	for i in range(clen):
		for j in range(i+1,clen):
			if(df_corr.iloc[i][j] > 0.78):
				print(df_corr.columns[i], df_corr.columns[j],df_corr.iloc[i][j])


##############################################################

def correlation_matrix(log_data):

	newdata = log_data.iloc[:63]
	df_corr = newdata.corr()
	df_corr.to_csv('correlation_matrix.csv')

	# print(df_corr)
	# print()

	return df_corr

#############################################################

def create_close_csv(list_of_stocks):

	# Year-Month-Day
	start_date = '2021-03-04'
	end_date = '2023-03-04'

	data = pd.DataFrame()

	for ticker in list_of_stocks:

		df = yf.download(ticker, start_date, end_date)
		list_ = [round(x,2) for x in df['Close']]
		data[ticker] = list_[::-1]

	data.index = df.index[::-1]

	data.to_csv('Energy_close.csv')

	return data

############################################################

def plotting_graphs(xom_cvx_data):

	xom_cvx_data['XOM'].plot(label = 'XOM', figsize = (10,7))
	xom_cvx_data['CVX'].plot(label = 'CVX', figsize = (10,7))
	xom_cvx_data['Spread'].plot(label = 'Spread', figsize = (10,7))

	plt.title('XOM vs CVX', fontsize = 16)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('Price', fontsize = 14)

	plt.grid(which = 'major', linestyle = '-.', linewidth = 0.5)

	plt.legend()

	plt.show()

############################################################

def stats(close_data, log_data):

	column_names = list(log_data.columns)[1:]

	df = pd.DataFrame()

	for col in column_names:
		list_ = []
		list_20 = log_data[col].tolist()[:20]
		list_60 = log_data[col].tolist()[:62]
		list_.append(sum(list_20)/20)
		list_.append(sum(list_60)/62)
		list_.append(statistics.stdev(list_20))
		list_.append(statistics.stdev(list_60))
		list_.append(sum(close_data[col].tolist()[:20])/20)
		list_.append(sum(list_20))

		df[col] = list_
	
	df.to_csv('stats.csv')

############################################################

list_of_stocks = ['XOM', 'CVX', 'MRO', 'PSX', 'VLO', 'SLB', 'HAL', 'OXY', 'EQT']

close_data = create_close_csv(list_of_stocks)
log_data, close_log_data = log_columns(close_data)
xom_cvx_data, combined_data = create_xom_cvx_data(close_data, log_data, close_log_data)
log_corr = correlation_matrix(log_data)
top_corr(log_corr)
plotting_graphs(xom_cvx_data)
stats(close_data, log_data)
