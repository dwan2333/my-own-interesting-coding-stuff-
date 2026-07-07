import os
# This clears the proxy settings specifically for this Python script so yfinance can connect to the internet!
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['ALL_PROXY'] = ''

import yfinance as yf
from pathlib import Path

# Get SpaceX data (using the ticker from your image)
spcx = yf.Ticker("SPCX")

# Download 1 year of historical data and save it to a CSV
data = spcx.history(period="1y")
data.to_csv("SPCX_historical_data.csv")
