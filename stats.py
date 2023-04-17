

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import statistics
import math
import sys


######################################################

def attach_log_column(data):
	log_column = [0]
	adj_column = data['Close'].tolist()

	for i in range(1,len(adj_column)):
		div_val = adj_column[i]/adj_column[i-1]
		log_column.append(math.log(div_val))

	data = data.assign(Log_Column=log_column)

	return data


##################################################

def list_singlesecstats(list_of_stocks):

	start_date = datetime.now() - timedelta(days = 100, hours = datetime.now().hour)
	end_date = datetime.now() + timedelta(days = 1)

	data = pd.DataFrame(columns = ['Ticker', 'AVG_21', 'AVG_63', 'STD_DEV_21', 'STD_DEV_63', 'AVGP_21', 'RET_21', 'RET_SUM_21', 'RET_SUM_63', 'DIS_TR_21', 'DIS_TR_63', '21_RET', '63_RET', 'RPER_21', 'RPER_63'])
	data = data.set_index('Ticker')

	for sym in list_of_stocks:
		df = yf.download(sym, start_date, end_date)
		df = attach_log_column(df)

		list_ = df['Log_Column'].tolist()[::-1]
		avg_21 = sum(list_[:21])/21
		avg_63 = sum(list_[:63])/63
		ret_21 = sum(list_[:21])
		std_dev_21 = statistics.stdev(list_[:21])
		std_dev_63 = statistics.stdev(list_[:63])
		avgp_21 = sum((df['Close'][::-1])[:21])/21

		ret_sum_21 = sum([(c - o) for c in df['Close'][::-1][:21] for o in df['Open'][::-1][:21]])
		ret_sum_63 = ret_sum_21 + sum([(c - o) for c in df['Close'][::-1][21:63] for o in df['Open'][::-1][21:63]])

		dist_trav_21 = sum([math.sqrt((ret**2) + 1) for ret in list_[:21]])
		dist_trav_63 = dist_trav_21 + sum([math.sqrt((ret**2) + 1) for ret in list_[21:63]])

		return_21 = (list_[20] - list_[0])/ list_[0]
		return_63 = (list_[62] - list_[0])/ list_[0]

		rper_21 = (df['Close'][::-1][20] - df['Close'][::-1][0])/df['Close'][::-1][0]
		rper_63 = (df['Close'][::-1][62] - df['Close'][::-1][0])/df['Close'][::-1][0]

		data.loc[sym] = [avg_21, avg_63, std_dev_21, std_dev_63, avgp_21, ret_21, ret_sum_21, ret_sum_63, dist_trav_21, dist_trav_63, return_21, return_63, rper_21, rper_63]


	if(len(list_of_stocks) > 5):
		data.to_csv('single_sec_stats.csv')
	else:
		print(data.head(n = 5))


####################################################

list_of_stocks = []

if('.txt' in sys.argv[1]):

	f = open(sys.argv[1], 'r')
	line = f.readlines()

	list_of_stocks = line[0].split(' ')

else:

	list_of_stocks.append(sys.argv[1])

list_singlesecstats(list_of_stocks)



