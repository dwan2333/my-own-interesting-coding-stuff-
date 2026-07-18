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
    # making sure that the historical chart is not duplicated
if Path(Path.cwd()/f'{file_name}').exists():
    pass
else:
    data.to_csv(file_name)


# `data['Close']` actually returns a mini-table containing the ticker name (SPCX)
# We need to specify the ticker name to grab the actual column of numbers!

import csv 

csv_open = open(file_name)
csv_reading = csv.reader(csv_open)

close_price = []
for row in csv_reading:
    close_price.append(row[1])

return_calc = []
for i in range(len(close_price)):
    try:
        # CSV files are read as text strings, so we MUST convert them to numbers (floats) first!
        current_price = float(close_price[i])
        next_price = float(close_price[i+1])
        
        # Standard return formula: (New - Old) / Old
        returns = (next_price - current_price) / current_price
        return_calc.append(returns)
        
    except IndexError:
        # This catches the error when i+1 goes past the end of the list!
        pass
    except ValueError:
        # This catches the very first row (the word "Close") which can't be converted to a number
        pass

print(return_calc)
    

    





    










