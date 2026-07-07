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

## Key Takeaways

- **`yfinance` is third-party** (`pip install yfinance`) and pulls Yahoo Finance data into **pandas** structures; it's unofficial and network-dependent.
- **`yf.Ticker("SYM")`** = one symbol: `.history()` for prices, `.info` / `.fast_info` for company data, `.dividends`, `.financials`, etc.
- **`yf.download([...])`** = bulk price history for one or many symbols, controlled by `period` **or** `start`/`end`, plus `interval`.
- Everything comes back as a **DataFrame/Series** indexed by date — use pandas from there (`.mean()`, `.pct_change()`, `.to_csv()`).
- Docs: **GitHub README** for the quickstart, **ranaroussi.github.io/yfinance** for the full reference.

---

### Sources

| Source | Date | Type |
|---|---|---|
| yfinance — GitHub repository (`ranaroussi/yfinance`) | 2026 | Library documentation |
| yfinance — official docs site (`ranaroussi.github.io/yfinance`) | 2026 | API reference |
| Verified live against yfinance 1.5.1 on `E:\Python` | 2026-07-07 | Local test |
