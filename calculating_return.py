import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

import yfinance as yf

SPCA = yf.Ticker('SPCX')
data = yf.download('SPCX')
data.to_csv('spacex_historical_chart.csv')

