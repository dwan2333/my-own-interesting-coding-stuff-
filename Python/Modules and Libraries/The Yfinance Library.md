# The Yfinance Library

_Research compiled 2026-07-07 — third-party `yfinance` library for downloading market data from Yahoo Finance_

> Companion to [Random Modules](<Random Modules.md>) and [The Pyperclip Module](<The Pyperclip Module.md>). **`yfinance`** pulls stock, ETF, and index data from Yahoo Finance into **pandas DataFrames** — prices, dividends, company info, and more. It's the go-to free library for hobby/analysis financial data.

---

## Branch 1 — Install First (Not Built-In)

`yfinance` is third-party — install it before importing:

```bash
pip install yfinance
# on your machine:
E:\Python\python.exe -m pip install yfinance
# or via conda:  conda install -c conda-forge yfinance
```

```python
import yfinance as yf   # conventional alias
```

> [!note] Already installed here
> This vault's Python has **yfinance 1.5.1** and **pandas**, so the examples below run as-is.

> [!warning] Unofficial + network-dependent
> yfinance **scrapes** Yahoo Finance — it isn't an official API. That means (a) it needs an internet connection, and (b) it can break when Yahoo changes their site. If a call suddenly errors, update with `pip install -U yfinance` and check the project's GitHub issues.

---

## Branch 2 — Where the Documentation Lives

| Resource | What's there |
|---|---|
| **GitHub repo (README)** — `github.com/ranaroussi/yfinance` | Quickstart + copy-paste examples — best starting point |
| **Docs site** — `ranaroussi.github.io/yfinance` | Full API reference: every class, method, and parameter |
| **PyPI** — `pypi.org/project/yfinance` | Install command, version history |
| **GitHub Wiki** | FAQs, rate-limit and troubleshooting guides |

The **two things to look up first** are the `Ticker` class (one symbol) and `yf.download()` (bulk prices).

---

## Branch 3 — The `Ticker` Object (one symbol)

`yf.Ticker("SYMBOL")` gives you an object with everything about that one security.

```python
import yfinance as yf

aapl = yf.Ticker('AAPL')

# price history → a pandas DataFrame
hist = aapl.history(period='5d')
print(list(hist.columns))    # ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
print(hist['Close'].iloc[-1])  # most recent closing price
```

| Attribute / method | Returns |
|---|---|
| `.history(period=, interval=, start=, end=)` | price DataFrame (OHLCV + dividends/splits) |
| `.info` | big dict of company data (name, sector, market cap, …) |
| `.fast_info` | a lightweight, fast subset (`lastPrice`, `marketCap`, …) |
| `.dividends` | a pandas Series of dividend payments over time |
| `.splits` | stock-split history |
| `.actions` | dividends + splits combined |
| `.financials` / `.balance_sheet` / `.cashflow` | financial statements |

```python
import yfinance as yf

aapl = yf.Ticker('AAPL')
print(aapl.info['shortName'], '—', aapl.info['sector'])   # Apple Inc. — Technology
print(aapl.fast_info['lastPrice'])                        # quick last price
print(aapl.dividends.tail(3))                             # last 3 dividend payments
print(aapl.splits.tail(2))                                # recent stock splits (Series)
print(aapl.actions.columns.tolist())                      # ['Dividends', 'Stock Splits']
print(aapl.financials.shape)                              # income statement (DataFrame), e.g. (39, 5)
print(aapl.balance_sheet.shape)                           # balance sheet DataFrame
print(aapl.cashflow.shape)                                # cash-flow statement DataFrame
```

> [!tip] `.info` is heavy, `.fast_info` is light
> `.info` fetches a large dictionary and is slower; if you just need the current price or market cap, `.fast_info` is much faster.

---

## Branch 4 — `yf.download()` (many symbols at once)

`yf.download()` is the fastest way to grab price history for **one or many** tickers straight into a DataFrame.

```python
import yfinance as yf

# multiple tickers, by period
data = yf.download(['AAPL', 'MSFT'], period='5d', progress=False)
print(data.shape)        # (5, 10)  → 5 days × (5 fields × 2 tickers)

# one ticker, explicit date range and interval
one = yf.download('AAPL', start='2024-01-01', end='2024-12-31',
                  interval='1d', progress=False)

# auto_adjust=False keeps a separate 'Adj Close' column (default True folds it in)
raw = yf.download('AAPL', period='5d', auto_adjust=False, progress=False)
print('Adj Close' in raw.columns.get_level_values(0))   # True
```

Key arguments:

| Argument | Meaning |
|---|---|
| first arg | a symbol `'AAPL'` or a list `['AAPL', 'MSFT']` |
| `period=` | how far back: `'1d'`, `'5d'`, `'1mo'`, `'1y'`, `'max'`, … |
| `start=` / `end=` | explicit date range (`'YYYY-MM-DD'`) — use *instead* of `period` |
| `interval=` | bar size: `'1d'`, `'1h'`, `'5m'`, `'1wk'`, … |
| `progress=False` | hide the download progress bar |
| `auto_adjust=` | adjust prices for splits/dividends (default `True`) |

> [!warning] Intraday intervals have a limited window
> Fine intervals like `'1m'` / `'5m'` only reach back a short period (roughly the last 7–60 days, depending on interval). For years of data, use a daily `'1d'` (or coarser) interval.

---

## Branch 5 — It's All pandas

Everything yfinance returns is a **pandas DataFrame or Series**, so all your pandas tools apply immediately — a natural bridge into data analysis.

```python
import yfinance as yf

hist = yf.download('AAPL', period='1mo', progress=False)

print(hist['Close'].mean())            # average close over the month
print(hist['Close'].pct_change())      # daily % returns
hist['Close'].to_csv('aapl_close.csv') # save to a file
```

- The **index** is a `DatetimeIndex` (the dates).
- Columns are `Open`, `High`, `Low`, `Close`, `Volume` (plus `Dividends`, `Stock Splits` from `Ticker.history`).
- For multiple tickers, columns become a **two-level** (MultiIndex) header: field × ticker — e.g. `data['Close']['AAPL']`.

---

## Branch 6 — Downloading a Historical Chart (data → picture)

> [!important] yfinance gives you **data**, not a picture
> There's no "download the chart" button. yfinance downloads the historical **numbers** (a table of dates and prices); *you* then **plot** those numbers to draw the chart. So a "historical chart" is always **two steps**: (1) download the data, (2) plot it.

### Step 1 — download the historical data

```python
import yfinance as yf

# grab 6 months of daily AAPL prices → a pandas DataFrame
data = yf.download('AAPL', period='6mo', interval='1d', progress=False)
print(data.shape)          # e.g. (124, 5)  → 124 trading days
print(data['Close'].tail())  # the last few closing prices
```

### Step 2 — plot it into a chart

The quickest way is pandas' built-in `.plot()` (it wraps matplotlib):

```python
import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download('AAPL', period='6mo', progress=False)

data['Close'].plot(title='AAPL — 6-month close', figsize=(9, 4))
plt.savefig('aapl_chart.png', dpi=110, bbox_inches='tight')  # save the image
plt.show()                                                    # or pop it on screen
```

Or with matplotlib directly for more control:

```python
import yfinance as yf
import matplotlib.pyplot as plt

data = yf.download('AAPL', period='6mo', progress=False)
close = data['Close']

plt.figure(figsize=(9, 4))
plt.plot(close.index, close.values)     # x = dates, y = prices
plt.title('AAPL — 6-month close')
plt.xlabel('Date'); plt.ylabel('Price ($)')
plt.savefig('aapl_chart.png', dpi=110, bbox_inches='tight')
```

- **`.savefig('name.png')`** writes the chart to an image file.
- **`.show()`** opens it in a window (in the Obsidian runner or a plain terminal, prefer `savefig` — there's no pop-up window there).
- Want a candlestick chart instead of a line? Install **`mplfinance`** (`pip install mplfinance`) and call `mpf.plot(data, type='candle')`.

### Step 3 (optional) — save the raw data too

```python
data.to_csv('aapl_6mo.csv')     # keep the numbers as a CSV
# reload later with:  pandas.read_csv('aapl_6mo.csv', index_col=0, parse_dates=True)
```

---

## Branch 7 — Other Commonly Used Data

Beyond prices, a `Ticker` exposes lots more. These are the ones people reach for most:

| Access | Returns |
|---|---|
| `t.options` | tuple of option **expiry dates** available |
| `t.option_chain('YYYY-MM-DD')` | an object with `.calls` and `.puts` DataFrames for that expiry |
| `t.news` | a list of recent news items (dicts) about the ticker |
| `t.recommendations` | analyst buy/hold/sell recommendations (DataFrame) |
| `t.calendar` | upcoming events (earnings date, dividend date) |
| `t.earnings_dates` | past & upcoming earnings dates (DataFrame) |

```python
import yfinance as yf

t = yf.Ticker('AAPL')
print(t.options[:3])                       # e.g. ('2026-07-08', '2026-07-10', '2026-07-17')
chain = t.option_chain(t.options[0])       # first expiry
print(chain.calls.columns.tolist()[:5])    # ['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid']
print(len(t.news), 'news items')
```

### Multiple tickers as objects — `yf.Tickers`

`yf.download([...])` gives one combined DataFrame; `yf.Tickers(...)` instead gives you a **`Ticker` object per symbol** (so you can use `.info`, `.history()`, etc. on each):

```python
import yfinance as yf

group = yf.Tickers('AAPL MSFT GOOG')      # space-separated string
print(group.tickers['MSFT'].fast_info['lastPrice'])   # reach one symbol's object
```

---

## Key Takeaways

- **`yfinance` is third-party** (`pip install yfinance`) and pulls Yahoo Finance data into **pandas** structures; it's unofficial and network-dependent.
- **`yf.Ticker("SYM")`** = one symbol: `.history()` for prices, `.info` / `.fast_info` for company data, `.dividends`, `.financials`, etc.
- **`yf.download([...])`** = bulk price history for one or many symbols, controlled by `period` **or** `start`/`end`, plus `interval`.
- Everything comes back as a **DataFrame/Series** indexed by date — use pandas from there (`.mean()`, `.pct_change()`, `.to_csv()`).
- **A "historical chart" is two steps:** download the data, then **plot** it — `data['Close'].plot()` then `plt.savefig('chart.png')`. yfinance gives numbers, not a picture. (Use `mplfinance` for candlesticks.)
- Beyond prices: `.options` / `.option_chain()`, `.news`, `.recommendations`, `.calendar`, `.earnings_dates`; and `yf.Tickers('AAPL MSFT')` for one `Ticker` object per symbol.
- Docs: **GitHub README** for the quickstart, **ranaroussi.github.io/yfinance** for the full reference.

---

### Sources

| Source | Date | Type |
|---|---|---|
| yfinance — GitHub repository (`ranaroussi/yfinance`) | 2026 | Library documentation |
| yfinance — official docs site (`ranaroussi.github.io/yfinance`) | 2026 | API reference |
| Verified live against yfinance 1.5.1 on `E:\Python` | 2026-07-07 | Local test |
