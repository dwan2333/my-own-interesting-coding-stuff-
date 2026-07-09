# making sure that the system know that internet is not though a proxy
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

import yfinance as yf

# download the historical chart for your choice of stock
ticker = input("Please choose the ticker for the stock: ")
data = yf.download(ticker, interval = '1d', period = 'max')
file_name = f'{ticker}_historical_chart.csv'
data.to_csv(file_name)

import csv

target_file = open(file_name)
to_read_target = csv.reader(target_file)






    










