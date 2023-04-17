
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import sys
import yfinance as yf
import matplotlib.pyplot as plt



def correlation_plot(sector, ndays):

	e_date = datetime.now()
	s_date = datetime.now() - timedelta(days = ndays, hours = datetime.now().hour)

	log_data = pd.read_csv('log_data.csv')
	data =  pd.DataFrame()

	sector_syms = pd.read_csv('sectorwise_names.csv')
	symbols = sector_syms[sector].tolist()[:sector_syms.count()[sector] - 1]

	# symbols = ['JNJ', 'BMY', 'AMGN', 'LLY', 'MRK', 'GILD', 'BIIB', 'ABBV', 'OGN', 'PFE']

	for sym in symbols:

		data[sym] = log_data['Log_'+sym]


	data_corr = data.corr()

	data_corr.to_csv('heath_corr.csv')

	plt.figure(figsize = (10,7))
	hm = sns.heatmap(data_corr, annot = False)
	plt.show()


############################################################

def rearrange(df_corr):

	symbols = df_corr.index.tolist()



############################################################

correlation_plot(sys.argv[1], int(sys.argv[2]))
