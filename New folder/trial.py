
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import statistics 


def stats(close_data, log_data):

	column_names = list(log_data.columns)[1:]

	df = pd.DataFrame()

	for col in column_names:
		list_ = []
		list_30 = log_data[col].tolist()[:20]
		list_60 = log_data[col].tolist()[:62]
		list_.append(sum(list_30)/20)
		list_.append(sum(list_60)/62)
		list_.append(statistics.stdev(list_30))
		list_.append(statistics.stdev(list_60))
		list_.append(sum(close_data[col].tolist()[:20])/20)
		list_.append(sum(list_30))

		df[col] = list_
	
	df.to_csv('stats.csv')


close_data = pd.read_csv('Energy_close.csv')
log_data = pd.read_csv('returns.csv')
stats(close_data,log_data)