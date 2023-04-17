
#autocorrelation 

import sys
import numpy as np 
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math

######################################################

def attach_log_column(data):
	log_column = [0]
	adj_column = data['Close'].tolist()

	for i in range(1,len(adj_column)):
		div_val = adj_column[i]/adj_column[i-1]
		log_column.append(math.log(div_val))

	data = data.assign(Log_Column=log_column)

	return data

#######################################################

def correlation_of_two_columns(list_1, list_2):

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

######################################################

def autocorrelation(sym, ndays, no_of_days):

	end_date = datetime.now()
	start_date = end_date - timedelta(days = ndays, hours = datetime.now().hour)

	auto_corr = [None for i in range(no_of_days)]

	df = yf.download(sym, start_date, end_date)
	df = attach_log_column(df)

	list_ = df['Log_Column'].tolist()

	for i in range(len(list_) - (no_of_days)):

		list_1 = list_[i : i + no_of_days]
		list_2 = list_[i + 1 : i + 1 + no_of_days]

		cor = correlation_of_two_columns(list_1, list_2)
		auto_corr.append(cor)

	df['Auto_corr'] = auto_corr
	df.to_csv('auto_corr_column.csv')


	plt.figure(figsize = (10,7))
	plt.plot(df.index, auto_corr, label = 'Auto_cor ['+ str(no_of_days) + ' days]', linestyle = '-')
	plt.title(label = 'Autocorrelation of ' + sym + '[Log_col]', fontsize = 15)

	plt.legend()
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('Auto_Cor', fontsize = 14)
	plt.grid(which = 'major', linestyle = '-.', linewidth = 0.5)

	plt.show()

#######################################################################

autocorrelation(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))