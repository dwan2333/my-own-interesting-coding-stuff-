import sys
import subprocess

# This forces the specific Python environment your editor is using right now to install yfinance
print("Current editor python path:", sys.executable)
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'yfinance'])

# Now try importing it
import yfinance as yf
print("Successfully imported yfinance version:", yf.__version__)
