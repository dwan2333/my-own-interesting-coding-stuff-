# making sure that the system know that internet is not though a proxy
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

import yfinance as yf

# download the historical chart for your choice of stock
from pathlib import Path
ticker = input("Please choose the ticker for the stock: ")
data = yf.download(ticker, interval = '1d', period = 'max')
file_name = f'{ticker}_historical_chart.csv'
if Path(Path.cwd()/f'{file_name}').exists():
    pass
else:
    data.to_csv(file_name)


# `data['Close']` actually returns a mini-table containing the ticker name (SPCX)
# We need to specify the ticker name to grab the actual column of numbers!
close_price = data['Close'][ticker].tolist()

ticker_hist = yf.Ticker(f'{ticker}')

hist = ticker_hist.history(period = 'max')

print(hist['Close'].iloc[-2])


    





    










