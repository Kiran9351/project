
import pandas as pd 
import numpy as np
from datetime import datetime
import yfinance as yf
import math

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

company_data = pd.read_csv('Company_names.csv')

close_data = pd.DataFrame()
log_data = pd.DataFrame()
cdata = pd.DataFrame()
ldata = pd.DataFrame()

start_date = '2010-01-01'
end_date = datetime.now()

tickers = company_data['Symbol'].tolist()

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

close_data.to_csv('close_data.csv')
log_data.to_csv('log_data.csv')

################################################################

