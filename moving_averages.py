
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys

def moving_averages(stock_name, tdays, mdays):

	data = pd.read_csv('log_data.csv')
	data = data.set_index('Date')
	data.index = pd.to_datetime(data.index, format = '%Y-%m-%d %H:%M:%S')
	ldata = data['Log_'+stock_name].to_list()[::-1]

	all_sum = ldata[0]
	all_avg = 0
	m_sum = sum(ldata[:mdays-1])

	moving_avg = [None for i in range(mdays-1)]
	all_time_avg = [0]

	for i in range(1,len(ldata)):

		all_sum = all_sum + ldata[i]
		all_avg = all_sum/(i+1)
		all_time_avg.append(all_avg)

		if(i >= mdays - 1):
			m_sum = m_sum + ldata[i]
			m_avg = m_sum/mdays
			moving_avg.append(m_avg)
			m_sum = m_sum - ldata[i - (mdays-1)]

	df = pd.DataFrame()
	df.index = data.index
	df['Log_'+stock_name] = data['Log_'+stock_name]
	df['all_time_avg'] = all_time_avg[::-1]
	df['moving_avg'] = moving_avg[::-1]
	df.to_csv('df_combine.csv')


	plt.figure(figsize = (10,7))
	# data['Log_'+stock_name].plot(label = 'Daily_return')
	plt.plot(data.index, all_time_avg[::-1], label = 'all_time_avg')
	plt.plot(data.index, moving_avg[::-1], label = 'Moving_avg')
	# df['Log_'+stock_name].plot(label = 'return')
	# df['All_time_avg'].plot(label = 'All_time_avg')
	# df['moving_averages'].plot(label = 'moving_avg')
	plt.title('all_time_avg & Moving_avg plotting', fontsize = 16)
	plt.xlabel('Year', fontsize = 14)
	plt.ylabel('Avg return', fontsize = 14)

	plt.legend()
	plt.grid(which = 'major', linestyle = '-.', linewidth = 0.5)
	plt.show()

############################################################

moving_averages(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))