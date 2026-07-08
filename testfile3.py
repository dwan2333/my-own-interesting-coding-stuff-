import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

import yfinance as yf

data = yf.download('SPCX', period = 'max', interval = '1d' )

data.to_csv('Spacex_Historical_Chart.csv')

