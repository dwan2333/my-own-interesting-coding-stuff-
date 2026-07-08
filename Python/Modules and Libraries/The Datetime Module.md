# The Datetime Module

_Research compiled 2026-07-07 — Python standard library `datetime`_

> Part of the [Python Reference](<../Python Reference (Main).md>). The **`datetime`** module handles **dates and times** — storing them, doing arithmetic (how many days until X?), and converting to and from text. It's built in, so just `import datetime` (or import the specific classes).

---

## Branch 1 — The Four Main Classes

The module gives you four building blocks. Import just the ones you need:

```python
from datetime import date, time, datetime, timedelta
```

| Class | Represents | Example meaning |
|---|---|---|
| `date` | a calendar day | 2026-07-07 |
| `time` | a time of day | 14:30:05 |
| `datetime` | a day **and** a time together | 2026-07-07 14:30:05 |
| `timedelta` | a **duration** (a length of time) | 7 days, 3 hours |

The first three are *points* on the calendar/clock; `timedelta` is the *distance* between two of them.

---

## Branch 2 — Making Dates and Times

### Build a specific one

Pass the numbers in order: year, month, day (then hour, minute, second for a `datetime`).

```python
from datetime import date, datetime

d = date(2026, 7, 7)
print(d)                       # 2026-07-07

dt = datetime(2026, 7, 7, 14, 30, 5)
print(dt)                      # 2026-07-07 14:30:05
```

### Get the current one

| Call | Returns |
|---|---|
| `date.today()` | today's date |
| `datetime.now()` | right now (date + time) |

```python
from datetime import date, datetime

print(date.today())            # e.g. 2026-07-07  (whatever today is)
print(datetime.now())          # e.g. 2026-07-07 09:15:42.123456
```

---

## Branch 3 — Reading the Pieces Out

Every date/datetime lets you pull out its parts as plain numbers.

| Attribute | From | Example value |
|---|---|---|
| `.year` `.month` `.day` | date or datetime | 2026, 7, 7 |
| `.hour` `.minute` `.second` | time or datetime | 14, 30, 5 |
| `.weekday()` | date or datetime | 0=Monday … 6=Sunday |
| `.isoweekday()` | date or datetime | 1=Monday … 7=Sunday |

```python
from datetime import datetime

dt = datetime(2026, 7, 7, 14, 30, 5)
print(dt.year, dt.month, dt.day)     # 2026 7 7
print(dt.hour, dt.minute)            # 14 30
print(dt.weekday())                  # 1   (Tuesday — Monday is 0)
print(dt.isoweekday())               # 2   (Tuesday — Monday is 1)
```

> [!warning] `weekday()` vs `isoweekday()`
> `weekday()` counts **Monday as 0** (Sunday = 6); `isoweekday()` counts **Monday as 1** (Sunday = 7). Pick the one whose numbering you expect, or off-by-one bugs sneak in.

---

## Branch 4 — Time Arithmetic With `timedelta`

A `timedelta` is a **duration**. Add or subtract it from a date/datetime to move forward or backward in time; subtract two dates to get the duration between them.

```python
from datetime import date, datetime, timedelta

dt = datetime(2026, 7, 7, 14, 30, 5)
week_later = dt + timedelta(days=7, hours=3)
print(week_later)                    # 2026-07-14 17:30:05

# subtract two dates → a timedelta; read .days from it
gap = date(2026, 12, 25) - date(2026, 7, 7)
print(gap.days)                      # 171   (days until Christmas)
```

- `timedelta(days=, hours=, minutes=, seconds=, weeks=)` — combine any of these.
- Subtracting two dates gives a `timedelta`; its **`.days`** is the whole-day count.

---

## Branch 5 — Dates ↔ Text

Computers store dates as numbers, but you read and type them as text. Two methods bridge the gap:

| Method | Direction | Meaning |
|---|---|---|
| `.strftime(format)` | date → **str** | **f** = format: make a string for humans |
| `datetime.strptime(text, format)` | **str** → datetime | **p** = parse: read a string into a datetime |

```python
from datetime import datetime

dt = datetime(2026, 7, 7, 14, 30, 5)

# strftime — format a datetime into readable text
print(dt.strftime('%A, %B %d, %Y at %I:%M %p'))
# Tuesday, July 07, 2026 at 02:30 PM

# strptime — parse text back into a datetime
parsed = datetime.strptime('2026-07-07 14:30', '%Y-%m-%d %H:%M')
print(parsed)                        # 2026-07-07 14:30:00
```

### The common format codes

| Code | Means | Example |
|---|---|---|
| `%Y` / `%y` | 4-digit / 2-digit year | 2026 / 26 |
| `%m` | month number | 07 |
| `%B` / `%b` | month name / short | July / Jul |
| `%d` | day of month | 07 |
| `%A` / `%a` | weekday name / short | Tuesday / Tue |
| `%H` / `%I` | hour (24h / 12h) | 14 / 02 |
| `%M` `%S` | minute, second | 30, 05 |
| `%p` | AM / PM | PM |

> [!tip] `isoformat()` for a standard text form
> `dt.isoformat()` gives the machine-standard `'2026-07-07T14:30:05'` — great for saving to files or databases, and `datetime.fromisoformat(...)` reads it straight back.

```python
from datetime import datetime
dt = datetime(2026, 7, 7, 14, 30, 5)
print(dt.isoformat())                # 2026-07-07T14:30:05
```

---

## Branch 6 — Combining date + time

If you have a `date` and a `time` separately, `datetime.combine()` merges them:

```python
from datetime import date, time, datetime

d = date(2026, 7, 7)
t = time(9, 0)
print(datetime.combine(d, t))        # 2026-07-07 09:00:00
```

---

## Key Takeaways

- Four classes: **`date`** (a day), **`time`** (a time of day), **`datetime`** (both), and **`timedelta`** (a duration).
- Build one with numbers — `date(2026, 7, 7)` — or get the current moment with **`date.today()`** / **`datetime.now()`**.
- Read parts with `.year`/`.month`/`.day`/`.hour`… and the weekday with **`.weekday()`** (Mon=0) or **`.isoweekday()`** (Mon=1).
- Do time math with **`timedelta`**: add it to move in time; subtract two dates to get the gap (read **`.days`**).
- Convert to/from text with **`.strftime(fmt)`** (format out) and **`datetime.strptime(text, fmt)`** (parse in); **`.isoformat()`** for the standard machine form.

---

### Sources

| Source | Date | Type |
|---|---|---|
| Python `datetime` — official documentation | 2026 | Standard library reference |
| Verified against Python 3.14 on `E:\Python` | 2026-07-07 | Local test |
