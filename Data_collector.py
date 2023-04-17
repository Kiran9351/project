
import pandas as pd 
import numpy as np
import yfinance as yf
from datetime import datetime

df = pd.read_csv('company_names.csv')
symbols = df['Symbol'].tolist()
names = df['Company'].tolist()

start_date = '2010-01-01'
end_date = datetime.now()

i = 0

for i in range(len(names)):
	data = yf.download(symbols[i],start_date, end_date)
	name = names[i]
	name = name.replace(' ','_')
	data.to_csv(name+".csv")

