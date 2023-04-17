
import pandas as pd
import numpy as np

sectors = pd.read_csv('sectors.csv')

cdata = pd.read_csv('Company_names.csv')
symbols = cdata['Symbol'].tolist()

sectorwise = pd.DataFrame()
syms = []

for col in sectors:

	for sym in sectors[col]:
		if sym in symbols:
			syms.append(sym)


	sectorwise[col] = pd.Series(syms)
	syms = []

sectorwise.to_csv('sectorwise_names.csv')