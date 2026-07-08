# making sure that the system know that internet is not though a proxy
from msilib.schema import Error
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

# fetch the historical chart from yahoo in csv
import yfinance as yf

import csv

# download the historical chart for your choice of stock
ticker = 'SPCX'
try:
    data = yf.download(ticker)
    data.to_csv(f'{ticker}_historical_chart.csv')
except Error:
    pass

open(f'{ticker}_historical_chart.csv')







