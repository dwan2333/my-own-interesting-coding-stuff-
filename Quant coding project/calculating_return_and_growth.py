# imports of various module for later use 
import yfinance as yf
import os
from pathlib import Path
# making sure that the system know that internet is not though a proxy
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''



# automatically download the historical chart for your choice of stock
print('Please type in your choice of stock symbol or ticker')
ticker = (input(">>> ")).strip()
data = yf.download(ticker, interval = '1d', period = 'max')
file_name = f'{ticker}_historical_chart.csv'
# making sure that the historical chart is not duplicated
if Path(Path.cwd()/f'{file_name}').exists():
    pass
else:
    data.to_csv(file_name)


# csv module imported for gathering close_price and return_price
import csv 
csv_open = open(file_name)
csv_reading = csv.reader(csv_open)

close_price = list()
return_calc = list()

# filter non int variables inside close_price
for row in csv_reading:
    try:
        # Convert directly to float while reading. 
        # If it's a header or empty, it will throw an error and be ignored.
        close_price.append(float(row[1]))
    except (ValueError, IndexError):
        pass

# commands to return a list for percentile returns each consecutive days
for i in range(len(close_price)):
    try:
        # CSV files are read as text strings, so we MUST convert them to numbers (floats) first!
        current_price = close_price[i]
        next_price = close_price[i+1]
        
        # Standard return formula: (New - Old) / Old
        returns = (next_price - current_price) / current_price
        return_calc.append(returns)
    except IndexError:
        # This catches the error when i+1 goes past the end of the list!
        pass



    
# function with given list of your total investment return for each day
def growth(returns, investment = 1):

    everyday_returns = list() 

    for x in returns: 
        investment *= (1 + x)
        everyday_returns.append(investment)

    return everyday_returns

# function to return the simple moving average with your choice in windows size
def simple_moving_average(close_price,window = 3):

    columns = list()

    assert window < len(close_price), 'Your window size is larger than the date values itself !'

    # based on user intended windows size, make the close_price into a nested list for later calculation of sma
    for i in range(len(close_price)):
        if i != 1 + len(close_price) - window:
            columns.append(close_price[i:window+i]) 
        else:
            break

    result = list(map(lambda x: sum(x)/3, columns))

    return result 







    

    
            





    










