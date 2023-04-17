
import pandas as pd 
import numpy as np
from datetime import datetime
import yfinance as yf
import math

start_date = '2021-01-01'
end_date = datetime.now()

df = yf.download('AAPL', start_date, end_date)
df = df[::-1]
df.to_csv('check_data.csv')