# making sure that the system know that internet is not though a proxy
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
ticker = input("Please choose the ticker for the stock: ")
file_name = f'{ticker}_historical_chart'

print(file_name)
    










