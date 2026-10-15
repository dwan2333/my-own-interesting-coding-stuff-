# Chapter 1 Exercises — Abstract Data Types

_Rance D. Necaise, *Data Structures and Algorithms Using Python*, Chapter 1 · all 4 exercises and 11 programming projects, with tested solutions_

> [!info] What's in this note
> Every end-of-chapter problem from Chapter 1, in the book's order. Exercises 1.1–1.4 grow one `Date` class. Programming Projects 1.1–1.11 build ten more small ADTs with the chapter's habits: protected `_attributes`, `assert` for preconditions, and Python operators for "comparable", "toString", "length" and "iterator". Try each problem first, then click **Click to reveal solution**.
>
> **How it was tested.** Every solution was saved as a `.py` file and run with `python` (Python 3.14, Windows). Each **Check** block is pasted from that run. Exercises 1.1, 1.2 and 1.4 build one shared `date.py`, which Exercise 1.3 and Projects 1.7 and 1.10 import. Extra tests, not shown: `Date` was compared with Python's `datetime` on about 100,000 dates from year 1 to 9999, `Fraction` with Python's `fractions` on 20,000 random pairs, and `intersects()` with a brute-force check on 58,574 random segment pairs. All agreed.
>
> Where you already wrote a version in `Small Coding Projects`, the problem names your file so you can compare.

---

## Exercises

> [!example] Exercise 1.1 — Finish the Date Class
> **Problem.** The chapter's `Date` class (Listing 1.2) stores a date as one integer, its Julian day number, and leaves five methods unwritten. Write them:
> - `monthName()`: the month's name, e.g. `"May"`.
> - `isLeapYear()`: does this date fall in a leap year?
> - `numDays( otherDate )`: the number of days between this date and `otherDate`, as a positive integer.
> - `advanceBy( days )`: move the date forward (positive `days`) or back (negative `days`), but never before the calendar's first day.
> - `isValidGregorian()`: the helper the constructor calls (as `_isValidGregorian`) to decide whether a month, day and year form a real Gregorian date.
>
> **Your attempt:** `Small Coding Projects\Date ADT\DateADT.py`
>
> > [!success]- Click to reveal solution
> > **Approach.** Each method either reads the Gregorian parts back with `_toGregorian()` or does plain integer arithmetic on `_julianDay`. Three module-level helpers (`_isLeap`, `_daysInMonth`, `_toJulianDay`) serve the class here and in Exercise 1.2. Years use astronomical numbering, where year 0 is 1 BC, so the calendar's first day (Julian day 0, November 24, 4714 BC) prints as `11/24/-4713`.
> >
> > ```python
> > # date.py: the Date ADT, a proleptic Gregorian date stored as a Julian day number.
> >
> > _MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July",
> >                 "August", "September", "October", "November", "December")
> > _DAYS_IN_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
> >
> >
> > # Leap year: every 4th year, except century years not divisible by 400
> > # (2000 is a leap year, 1900 is not).
> > def _isLeap(year):
> >     return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
> >
> >
> > def _daysInMonth(month, year):
> >     if month == 2 and _isLeap(year):
> >         return 29
> >     return _DAYS_IN_MONTH[month - 1]
> >
> >
> > # Gregorian date -> Julian day number (Fliegel and Van Flandern's formula).
> > # t is -1 for January and February, else 0. The book's formula says
> > # t = (month - 14) / 12 rounded toward zero, but Python's // rounds down,
> > # so we set t directly instead.
> > def _toJulianDay(month, day, year):
> >     t = -1 if month < 3 else 0
> >     return (day - 32075
> >             + 1461 * (year + 4800 + t) // 4
> >             + 367 * (month - 2 - 12 * t) // 12
> >             - 3 * ((year + 4900 + t) // 100) // 4)
> >
> >
> > class Date:
> >     # Creates a date from Gregorian components. The date must be valid.
> >     def __init__(self, month, day, year):
> >         assert self._isValidGregorian(month, day, year), "Invalid Gregorian date."
> >         self._julianDay = _toJulianDay(month, day, year)
> >
> >     # The three Gregorian parts, worked out from the Julian day.
> >     def month(self):
> >         return self._toGregorian()[0]
> >
> >     def day(self):
> >         return self._toGregorian()[1]
> >
> >     def year(self):
> >         return self._toGregorian()[2]
> >
> >     def monthName(self):
> >         return _MONTH_NAMES[self.month() - 1]
> >
> >     # 0 = Monday ... 6 = Sunday. Julian day 0 was a Monday, and weekdays
> >     # repeat every 7 days, so the remainder after dividing by 7 is the answer.
> >     def dayOfWeek(self):
> >         return self._julianDay % 7
> >
> >     # Days between the two dates, always positive (or 0 for the same date).
> >     def numDays(self, otherDate):
> >         return abs(self._julianDay - otherDate._julianDay)
> >
> >     def isLeapYear(self):
> >         return _isLeap(self.year())
> >
> >     # Moves forward (days > 0) or back (days < 0), but never before the
> >     # calendar's first day, Julian day 0.
> >     def advanceBy(self, days):
> >         self._julianDay = max(0, self._julianDay + days)
> >
> >     def __str__(self):
> >         month, day, year = self._toGregorian()
> >         return f"{month:02d}/{day:02d}/{year:04d}"
> >
> >     # Comparing two dates is just comparing two integers.
> >     def __eq__(self, otherDate):
> >         return self._julianDay == otherDate._julianDay
> >
> >     def __lt__(self, otherDate):
> >         return self._julianDay < otherDate._julianDay
> >
> >     def __le__(self, otherDate):
> >         return self._julianDay <= otherDate._julianDay
> >
> >     # True if the three numbers form a real date on or after the calendar's
> >     # first day, 11/24/-4713 (4714 BC, because year 0 stands for 1 BC).
> >     # A @staticmethod needs no self: it checks plain numbers, not a Date.
> >     @staticmethod
> >     def _isValidGregorian(month, day, year):
> >         if not all(isinstance(part, int) for part in (month, day, year)):
> >             return False
> >         if not 1 <= month <= 12:
> >             return False
> >         if not 1 <= day <= _daysInMonth(month, year):
> >             return False
> >         return (year, month, day) >= (-4713, 11, 24)   # tuples compare left to right
> >
> >     # Julian day -> (month, day, year): the inverse of _toJulianDay.
> >     def _toGregorian(self):
> >         a = self._julianDay + 68569
> >         b = 4 * a // 146097
> >         a = a - (146097 * b + 3) // 4
> >         y = 4000 * (a + 1) // 1461001
> >         a = a - 1461 * y // 4 + 31
> >         m = 80 * a // 2447
> >         day = a - 2447 * m // 80
> >         a = m // 11
> >         month = m + 2 - 12 * a
> >         year = 100 * (b - 49) + y + a
> >         return month, day, year
> > ```
> >
> > Test script, `check_ex1_1.py`:
> >
> > ```python
> > from date import Date
> >
> > print("Julian day of 01/01/2000:", Date(1, 1, 2000)._julianDay)   # a peek, for testing only
> > print("10/15/1582 is weekday", Date(10, 15, 1582).dayOfWeek(), "(4 = Friday)")
> > print("Days from 05/15/1985 to 06/01/1988:", Date(6, 1, 1988).numDays(Date(5, 15, 1985)))
> > for year in (2000, 1900, 2024):
> >     print(year, "is a leap year:", Date(1, 1, year).isLeapYear())
> > print("Month of 05/15/1985:", Date(5, 15, 1985).monthName())
> >
> > d = Date(1, 30, 2024)
> > d.advanceBy(31)                       # crosses February 29
> > print("01/30/2024 + 31 days:", d)
> > d = Date(12, 25, 2023)
> > d.advanceBy(10)                       # crosses the year end
> > print("12/25/2023 + 10 days:", d)
> > d.advanceBy(-10)
> > print("then back 10 days:   ", d)
> > d = Date(11, 30, -4713)
> > d.advanceBy(-100)                     # would go before the first day
> > print("11/30/-4713 - 100 days:", d)
> >
> > for bad in ((2, 29, 2023), (4, 31, 2024), (13, 1, 2024)):
> >     try:
> >         Date(*bad)                    # *bad unpacks the tuple into 3 arguments
> >     except AssertionError as error:
> >         print(bad, "->", error)
> > ```
> >
> > **Check.** Output of `python check_ex1_1.py`:
> >
> > ```text
> > Julian day of 01/01/2000: 2451545
> > 10/15/1582 is weekday 4 (4 = Friday)
> > Days from 05/15/1985 to 06/01/1988: 1113
> > 2000 is a leap year: True
> > 1900 is a leap year: False
> > 2024 is a leap year: True
> > Month of 05/15/1985: May
> > 01/30/2024 + 31 days: 03/01/2024
> > 12/25/2023 + 10 days: 01/04/2024
> > then back 10 days:    12/25/2023
> > 11/30/-4713 - 100 days: 11/24/-4713
> > (2, 29, 2023) -> Invalid Gregorian date.
> > (4, 31, 2024) -> Invalid Gregorian date.
> > (13, 1, 2024) -> Invalid Gregorian date.
> > ```
> >
> > Julian day 2451545, Friday = 4, 1113 days, the three leap years, the month-end and year-end crossings, and the cap at the first day all come out right ✓
> >
> > **Insight.** Storing one integer makes the hard operations easy: comparing, `numDays` and `advanceBy` are one line each, and even `dayOfWeek` is just `_julianDay % 7` (simpler than the chapter's formula). The cost moves into the two conversion formulas, which are written once and hidden behind the interface.

> [!example] Exercise 1.2 — More Date Operations
> **Problem.** Add six operations to `Date`:
> - `dayOfWeekName()`: the weekday's name, e.g. `"Monday"`.
> - `dayOfYear()`: the date's position in its year (February 1 is day 32).
> - `isWeekday()`: is it Monday to Friday?
> - `isEquinox()`: is it the spring or autumn equinox?
> - `isSolstice()`: is it the summer or winter solstice?
> - `asGregorian( divchar = '/' )`: like `str()`, but with `divchar` between the month, day and year.
>
> **Your attempt:** `Small Coding Projects\Date ADT\DateADT.py` (the same file)
>
> > [!success]- Click to reveal solution
> > **Approach.** Add these methods at the end of the `Date` class in `date.py`. `dayOfYear()` subtracts the Julian day of January 1, using `_toJulianDay` from Exercise 1.1. The equinox and solstice tests use fixed approximate dates (March 20, June 21, September 22, December 21); the real dates shift by a day or so from year to year, so an exact answer would need an astronomy formula.
> >
> > ```python
> >     def dayOfWeekName(self):
> >         names = ("Monday", "Tuesday", "Wednesday", "Thursday",
> >                  "Friday", "Saturday", "Sunday")
> >         return names[self.dayOfWeek()]
> >
> >     # January 1 is day 1: count the days since January 1, then add one.
> >     def dayOfYear(self):
> >         return self._julianDay - _toJulianDay(1, 1, self.year()) + 1
> >
> >     def isWeekday(self):
> >         return self.dayOfWeek() < 5          # 0..4 = Monday..Friday
> >
> >     # Fixed approximate dates. The real equinoxes and solstices move
> >     # by a day or so from year to year.
> >     def isEquinox(self):
> >         return self._toGregorian()[:2] in ((3, 20), (9, 22))     # (month, day)
> >
> >     def isSolstice(self):
> >         return self._toGregorian()[:2] in ((6, 21), (12, 21))
> >
> >     def asGregorian(self, divchar='/'):
> >         month, day, year = self._toGregorian()
> >         return f"{month:02d}{divchar}{day:02d}{divchar}{year:04d}"
> > ```
> >
> > Test script, `check_ex1_2.py`:
> >
> > ```python
> > from date import Date
> >
> > for d in (Date(2, 1, 2026), Date(3, 20, 2026), Date(6, 21, 2026), Date(12, 31, 2024)):
> >     print(d.asGregorian("-"), f"{d.dayOfWeekName():<9}",
> >           f"day {d.dayOfYear():3d}",
> >           f" weekday {d.isWeekday()!s:<5}",          # !s turns True/False into text
> >           f" equinox {d.isEquinox()!s:<5}",
> >           f" solstice {d.isSolstice()}")
> > print(Date(7, 4, 2026).asGregorian(), Date(7, 4, 2026).asGregorian("."))
> > ```
> >
> > **Check.** Output of `python check_ex1_2.py`:
> >
> > ```text
> > 02-01-2026 Sunday    day  32  weekday False  equinox False  solstice False
> > 03-20-2026 Friday    day  79  weekday True   equinox True   solstice False
> > 06-21-2026 Sunday    day 172  weekday False  equinox False  solstice True
> > 12-31-2024 Tuesday   day 366  weekday True   equinox False  solstice False
> > 07/04/2026 07.04.2026
> > ```
> >
> > February 1 is day 32, and December 31, 2024 is day 366 because 2024 is a leap year ✓
> >
> > **Insight.** The new operations are built from ones that already exist (`dayOfWeek`, `_toGregorian`, `_toJulianDay`), so the storage didn't change at all. An ADT's interface can grow without touching its insides.

> [!example] Exercise 1.3 — Print a Month Calendar
> **Problem.** Write a function `printCalendar()` that takes a `Date` and prints a calendar for that date's month: the month name and year as a title, a row of day headings from Sunday to Saturday (`Su Mo Tu We Th Fr Sa`), then the day numbers lined up under their weekdays. The book's example uses the date 11/5/2007.
>
> **Your attempt:** `Small Coding Projects\Date ADT\Calender.py`
>
> > [!success]- Click to reveal solution
> > **Approach.** Start at the 1st of the month and step forward with `advanceBy(1)` until the month changes; each row is a list of 2-character cells joined by spaces. The one tricky part is the first row: `dayOfWeek()` counts from Monday = 0, but the columns start on Sunday, so the number of blank cells is `(dayOfWeek() + 1) % 7`.
> >
> > ```python
> > # printcal.py: print a month calendar for any Date (Exercise 1.3).
> > from date import Date
> >
> >
> > def printCalendar(date):
> >     day = Date(date.month(), 1, date.year())          # start on the 1st
> >     print(f"{day.monthName()} {day.year()}".center(20).rstrip())
> >     print("Su Mo Tu We Th Fr Sa")
> >     # dayOfWeek() runs Monday = 0 ... Sunday = 6, but our week starts on
> >     # Sunday, so shift by one: Sunday -> column 0, Monday -> column 1, ...
> >     week = ["  "] * ((day.dayOfWeek() + 1) % 7)        # blanks before the 1st
> >     while day.month() == date.month():
> >         week.append(f"{day.day():2d}")
> >         if len(week) == 7:                             # Saturday: end the row
> >             print(" ".join(week))
> >             week = []
> >         day.advanceBy(1)
> >     if week:
> >         print(" ".join(week))
> >
> >
> > if __name__ == "__main__":
> >     printCalendar(Date(11, 5, 2007))
> >     print()
> >     printCalendar(Date(2, 14, 2026))                   # a month that starts on Sunday
> > ```
> >
> > **Check.** Output of `python printcal.py`:
> >
> > ```text
> >    November 2007
> > Su Mo Tu We Th Fr Sa
> >              1  2  3
> >  4  5  6  7  8  9 10
> > 11 12 13 14 15 16 17
> > 18 19 20 21 22 23 24
> > 25 26 27 28 29 30
> >
> >    February 2026
> > Su Mo Tu We Th Fr Sa
> >  1  2  3  4  5  6  7
> >  8  9 10 11 12 13 14
> > 15 16 17 18 19 20 21
> > 22 23 24 25 26 27 28
> > ```
> >
> > November 1, 2007 lands under **Th** (it was a Thursday), and February 1, 2026, a Sunday, lands in the first column ✓
> >
> > **Insight.** `printCalendar()` is client code: it uses only public operations (`month()`, `day()`, `dayOfWeek()`, `advanceBy()`, `monthName()`) and never touches `_julianDay`, so it would still work if `Date` stored its data some other way.

> [!example] Exercise 1.4 — Date() Means Today
> **Problem.** Change the constructor so all three arguments are optional, each defaulting to 0. Calling `Date()` with no arguments should create today's date. The book's hint says to use a `date()` function from the `time` module. No such function exists; what the hint means is the standard library's `datetime.date.today()`.
>
> **Your attempt:** `Small Coding Projects\Date ADT\DateADT.py` (the same file)
>
> > [!success]- Click to reveal solution
> > **Approach.** Add `import datetime` near the top of `date.py`, then replace the constructor with the one below. If all three arguments are 0, it fills them in from `datetime.date.today()`. The usual validity check runs afterwards, so a half-given date like `Date(5)` is still rejected.
> >
> > ```python
> >     # Creates a date. Date() with no arguments (all zero) gives today's date.
> >     def __init__(self, month=0, day=0, year=0):
> >         if month == 0 and day == 0 and year == 0:
> >             today = datetime.date.today()
> >             month, day, year = today.month, today.day, today.year
> >         assert self._isValidGregorian(month, day, year), "Invalid Gregorian date."
> >         self._julianDay = _toJulianDay(month, day, year)
> > ```
> >
> > Test script, `check_ex1_4.py`:
> >
> > ```python
> > import datetime
> > from date import Date
> >
> > print("Date()            ->", Date())
> > print("datetime says     ->", datetime.date.today().strftime("%m/%d/%Y"))
> > print("Date(11, 5, 2007) ->", Date(11, 5, 2007))
> > try:
> >     Date(5)                     # only some arguments: day 0 is not a real date
> > except AssertionError as error:
> >     print("Date(5)           ->", error)
> > ```
> >
> > **Check.** Output of `python check_ex1_4.py`, run on October 15, 2026:
> >
> > ```text
> > Date()            -> 10/15/2026
> > datetime says     -> 10/15/2026
> > Date(11, 5, 2007) -> 11/05/2007
> > Date(5)           -> Invalid Gregorian date.
> > ```
> >
> > `Date()` agrees with `datetime` ✓
> >
> > **Insight.** Default arguments let one constructor serve two uses. The precondition check still sits in one place, after the defaults are filled in, so both ways of building a date are validated the same way.

---

## Programming Projects

> [!example] Project 1.1 — Counter ADT (a Clicker)
> **Problem.** A clicker counter is a small hand-held device with a display and two buttons: one adds 1 to the count shown, the other resets it to zero. Design a Counter ADT that works like one, and implement it.
>
> > [!success]- Click to reveal solution
> > **Approach.** The state is a single integer. Design:
> >
> > | Operation | What it does |
> > |---|---|
> > | `Counter()` | a new counter showing 0 |
> > | `click()` | the count button: add 1 (9999 rolls over to 0000, like a 4-digit display) |
> > | `reset()` | the reset button: back to 0 |
> > | `value()` | the number on the display |
> > | toString → `str()` | the display as 4 digits, e.g. `0042` |
> >
> > ```python
> > # counter.py: the Counter ADT, a hand-held clicker counter (Project 1.1).
> > _LIMIT = 10000          # a 4-digit display shows 0000 to 9999
> >
> >
> > class Counter:
> >     # Creates a counter that shows 0.
> >     def __init__(self):
> >         self._count = 0
> >
> >     # The count button: add one. After 9999 the display rolls over to 0000.
> >     def click(self):
> >         self._count = (self._count + 1) % _LIMIT
> >
> >     # The reset button.
> >     def reset(self):
> >         self._count = 0
> >
> >     # The number on the display.
> >     def value(self):
> >         return self._count
> >
> >     # The display as text, always 4 digits, e.g. "0042".
> >     def __str__(self):
> >         return f"{self._count:04d}"
> >
> >
> > if __name__ == "__main__":
> >     tally = Counter()
> >     for _ in range(3):
> >         tally.click()
> >     print("after 3 clicks:", tally, " value()", tally.value())
> >     tally.reset()
> >     print("after reset:   ", tally)
> >     for _ in range(_LIMIT):
> >         tally.click()
> >     print("after 10000 clicks:", tally, "(rolled over)")
> > ```
> >
> > **Check.** Output of `python counter.py`:
> >
> > ```text
> > after 3 clicks: 0003  value() 3
> > after reset:    0000
> > after 10000 clicks: 0000 (rolled over)
> > ```
> >
> > **Insight.** The operations copy the real device: its two buttons and its display. There is no way to set the count directly, just as on a real clicker. Rollover is a design decision, so the ADT's definition should state it.

> [!example] Project 1.2 — Grab Bag ADT
> **Problem.** Implement a Grab Bag ADT. It is the chapter's Bag with one change: there is no `remove()`. In its place, `grabItem()` removes and returns an item chosen at random.
>
> **Your attempt:** `Small Coding Projects\Bag_ADT.py` (its `grabItem()` method)
>
> > [!success]- Click to reveal solution
> > **Approach.** A list, like the chapter's Bag, because `random.randrange()` can pick any position in one step. `grabItem()` asserts the bag isn't empty, then swaps the chosen item to the end and pops it, so the items after it don't have to shift left.
> >
> > ```python
> > # grabbag.py: the Grab Bag ADT, a bag whose items come out at random (Project 1.2).
> > import random
> >
> >
> > class GrabBag:
> >     def __init__(self):
> >         self._theItems = list()
> >
> >     def __len__(self):
> >         return len(self._theItems)
> >
> >     def __contains__(self, item):
> >         return item in self._theItems
> >
> >     def add(self, item):
> >         self._theItems.append(item)
> >
> >     # Removes and returns a random item. The bag must not be empty.
> >     def grabItem(self):
> >         assert len(self._theItems) > 0, "Cannot grab from an empty bag."
> >         ndx = random.randrange(len(self._theItems))
> >         # A bag has no order, so swap the chosen item to the end and pop it:
> >         # no other items have to shift left to close the gap.
> >         items = self._theItems
> >         items[ndx], items[-1] = items[-1], items[ndx]
> >         return items.pop()
> >
> >     # A list's own iterator does the same job as the chapter's _BagIterator.
> >     def __iter__(self):
> >         return iter(self._theItems)
> >
> >
> > if __name__ == "__main__":
> >     random.seed(2026)                  # same "random" picks on every run
> >     bag = GrabBag()
> >     for name in ("Ana", "Ben", "Cai", "Dev", "Eli"):
> >         bag.add(name)
> >     print("'Dev' in bag:", "Dev" in bag, " size:", len(bag))
> >     while len(bag) > 0:
> >         print("grabbed", bag.grabItem(), "->", list(bag))
> >     try:
> >         bag.grabItem()
> >     except AssertionError as error:
> >         print("empty bag ->", error)
> > ```
> >
> > **Check.** Output of `python grabbag.py`:
> >
> > ```text
> > 'Dev' in bag: True  size: 5
> > grabbed Ana -> ['Eli', 'Ben', 'Cai', 'Dev']
> > grabbed Cai -> ['Eli', 'Ben', 'Dev']
> > grabbed Dev -> ['Eli', 'Ben']
> > grabbed Eli -> ['Ben']
> > grabbed Ben -> []
> > empty bag -> Cannot grab from an empty bag.
> > ```
> >
> > Each name comes out exactly once, in a random order, and grabbing from the empty bag fails its precondition ✓
> >
> > **Insight.** A bag promises no order, so the implementation may reorder items (the swap) to make removal cheap. An ADT that promised an order couldn't take this shortcut. `random.seed(2026)` only makes the demo repeatable.

> [!example] Project 1.3 — Counting Bag ADT
> **Problem.** Implement a Counting Bag ADT: the chapter's Bag plus `numOf( item )`, which returns how many copies of `item` the bag holds. Defend your choice of data structure.
>
> **Your attempt:** `Small Coding Projects\Bag_ADT.py` (its `numOf()` method)
>
> > [!success]- Click to reveal solution
> > **Approach.** Data structure: a dictionary from each distinct item to its count, plus a running total for `len()`. The chapter itself recommends this for a counting bag. `numOf()` becomes one lookup instead of a scan of every item, and 1,000 copies of one item take one entry instead of 1,000 list slots.
> >
> > ```python
> > # countingbag.py: the Counting Bag ADT (Project 1.3).
> > # Data structure: a dict that maps each distinct item to its number of copies.
> > class CountingBag:
> >     def __init__(self):
> >         self._counts = dict()       # item -> number of copies
> >         self._size = 0              # total items, duplicates included
> >
> >     def __len__(self):
> >         return self._size
> >
> >     def __contains__(self, item):
> >         return item in self._counts
> >
> >     def add(self, item):
> >         self._counts[item] = self._counts.get(item, 0) + 1
> >         self._size += 1
> >
> >     # Removes and returns one copy of item. The item must be in the bag.
> >     def remove(self, item):
> >         assert item in self._counts, "The item must be in the bag."
> >         self._counts[item] -= 1
> >         if self._counts[item] == 0:
> >             del self._counts[item]
> >         self._size -= 1
> >         return item
> >
> >     # How many copies of item the bag holds: one dict lookup, no scanning.
> >     def numOf(self, item):
> >         return self._counts.get(item, 0)
> >
> >     # A generator: `yield` hands out one item at a time, each item once per copy.
> >     def __iter__(self):
> >         for item, count in self._counts.items():
> >             for _ in range(count):
> >                 yield item
> >
> >
> > if __name__ == "__main__":
> >     bag = CountingBag()
> >     for fruit in ("apple", "pear", "apple", "fig", "apple"):
> >         bag.add(fruit)
> >     print("size", len(bag), " apples", bag.numOf("apple"), " plums", bag.numOf("plum"))
> >     bag.remove("apple")
> >     print("after remove: size", len(bag), " apples", bag.numOf("apple"), " 'fig' in bag:", "fig" in bag)
> >     print("items:", list(bag))
> > ```
> >
> > **Check.** Output of `python countingbag.py`:
> >
> > ```text
> > size 5  apples 3  plums 0
> > after remove: size 4  apples 2  'fig' in bag: True
> > items: ['apple', 'apple', 'pear', 'fig']
> > ```
> >
> > **Insight.** The same ADT can sit on different data structures; pick the one that makes the defining operation cheap. Trade-off: dictionary keys must be hashable, so this bag can't hold lists.

> [!example] Project 1.4 — Student Reader for a Comma-Separated File
> **Problem.** Write a new version of the Student File Reader ADT for a text file with one record per line and the five fields separated by commas, for example `10512, Maya, Chen, 2, 3.47` (id, first name, last name, class code, GPA). The operations stay the same: `StudentFileReader( filename )`, `open()`, `close()`, `fetchRecord()` and `fetchAll()`.
>
> **Your attempt:** `Small Coding Projects\Student_File_Reader_And_Writer.py` (its `fetchRecord_2()` method)
>
> > [!success]- Click to reveal solution
> > **Approach.** Only `fetchRecord()` changes: it reads one line, splits it at the commas and strips the spaces off each field. The class keeps the name `StudentFileReader`, so a program like the chapter's `studentreport.py` switches formats by changing only its import line. Blank lines are skipped, and `close()` and `fetchRecord()` assert that the file is open, as the ADT requires.
> >
> > ```python
> > # studentcsvfile.py: the Student File Reader ADT for a comma-separated file,
> > # one record per line:  id, first name, last name, class code, GPA  (Project 1.4)
> > class StudentFileReader:
> >     def __init__(self, inputSrc):
> >         self._inputSrc = inputSrc
> >         self._inputFile = None
> >
> >     def open(self):
> >         self._inputFile = open(self._inputSrc, "r")
> >
> >     def close(self):
> >         assert self._inputFile is not None, "The file is not open."
> >         self._inputFile.close()
> >         self._inputFile = None
> >
> >     def fetchAll(self):
> >         records = list()
> >         record = self.fetchRecord()
> >         while record is not None:
> >             records.append(record)
> >             record = self.fetchRecord()
> >         return records
> >
> >     # The only method that knows the file format: one line, split at the commas.
> >     def fetchRecord(self):
> >         assert self._inputFile is not None, "The file is not open."
> >         line = self._inputFile.readline()
> >         while line != "" and line.strip() == "":       # skip blank lines
> >             line = self._inputFile.readline()
> >         if line == "":                                  # end of the file
> >             return None
> >         fields = [field.strip() for field in line.split(",")]
> >         student = StudentRecord()
> >         student.idNum = int(fields[0])
> >         student.firstName = fields[1]
> >         student.lastName = fields[2]
> >         student.classCode = int(fields[3])
> >         student.gpa = float(fields[4])
> >         return student
> >
> >
> > # Storage class for one student record, the same as the chapter's.
> > class StudentRecord:
> >     def __init__(self):
> >         self.idNum = 0
> >         self.firstName = None
> >         self.lastName = None
> >         self.classCode = 0
> >         self.gpa = 0.0
> >
> >
> > if __name__ == "__main__":
> >     # Write a small sample file, then read it back.
> >     with open("students.csv", "w") as sample:
> >         sample.write("10512, Maya, Chen, 2, 3.47\n"
> >                      "10087, Omar, Haddad, 4, 3.92\n"
> >                      "10333, Lena, Brooks, 1, 2.85\n"
> >                      "10204, Ravi, Patel, 3, 3.10\n")
> >     reader = StudentFileReader("students.csv")
> >     reader.open()
> >     for student in reader.fetchAll():
> >         print(student.idNum, student.firstName, student.lastName,
> >               student.classCode, student.gpa)
> >     reader.close()
> > ```
> >
> > **Check.** Output of `python studentcsvfile.py`:
> >
> > ```text
> > 10512 Maya Chen 2 3.47
> > 10087 Omar Haddad 4 3.92
> > 10333 Lena Brooks 1 2.85
> > 10204 Ravi Patel 3 3.1
> > ```
> >
> > **Insight.** This is the chapter's promise kept: the file format lives in one method, and no code that uses the reader has to change.

> [!example] Project 1.5 — Student File Writer ADT
> **Problem.** The reader brings student records into a program; now build the matching writer for output.
> - (a) Design a Student File Writer ADT that outputs the records held in `StudentRecord` objects, either to a display or to storage.
> - (b) Implement it to print the records neatly on the terminal.
> - (c) Implement it to save the records to a text file in the chapter's format.
> - (d) Write a complete program that reads student records from a text file, sorts them by student id or by name (the user chooses), and shows them on the terminal with your writer.
>
> **Your attempt:** `Small Coding Projects\Student_File_Reader_And_Writer.py` (its `StudentFileWriter` class and `main()`)
>
> > [!success]- Click to reveal solution
> > **Approach.** (a) The writer mirrors the reader:
> >
> > | Operation | What it does |
> > |---|---|
> > | `StudentFileWriter( destination )` | creates a writer; where the output goes and its format depend on the implementation |
> > | `open()` | opens the connection to the output (the terminal version prints the table heading) |
> > | `close()` | finishes the output and closes it; the writer must be open |
> > | `writeRecord( record )` | outputs one `StudentRecord`; the writer must be open |
> > | `writeAll( records )` | outputs every record in a list, in order |
> >
> > (b) `StudentTerminalWriter()` and (c) `StudentTextFileWriter( filename )` are two implementations of these operations; a small base class gives both the same `writeAll()`. (d) reads the comma-separated file from Project 1.4, asks how to sort, then hands the records to both writers in one loop.
> >
> > ```python
> > # studentwriter.py: the Student File Writer ADT, two implementations (Project 1.5).
> > _CLASS_NAMES = (None, "Freshman", "Sophomore", "Junior", "Senior")
> >
> >
> > # Shared by both writers: writeAll() is writeRecord() in a loop.
> > class StudentWriter:
> >     def writeAll(self, records):
> >         for record in records:
> >             self.writeRecord(record)
> >
> >
> > # (b) Prints the records to the terminal as a neat table.
> > class StudentTerminalWriter(StudentWriter):
> >     def __init__(self):
> >         self._isOpen = False
> >         self._count = 0
> >
> >     def open(self):
> >         self._isOpen = True
> >         self._count = 0
> >         print()
> >         print("LIST OF STUDENTS".center(50).rstrip())
> >         print(f"{'ID':<5}  {'NAME':<25}  {'CLASS':<10}  {'GPA':>4}")
> >         print(f"{'-' * 5}  {'-' * 25}  {'-' * 10}  {'-' * 4}")
> >
> >     def writeRecord(self, record):
> >         assert self._isOpen, "The writer is not open."
> >         name = record.lastName + ", " + record.firstName
> >         className = _CLASS_NAMES[record.classCode]
> >         print(f"{record.idNum:<5}  {name:<25}  {className:<10}  {record.gpa:4.2f}")
> >         self._count += 1
> >
> >     def close(self):
> >         assert self._isOpen, "The writer is not open."
> >         print("-" * 50)
> >         print("Number of students:", self._count)
> >         self._isOpen = False
> >
> >
> > # (c) Saves the records to a text file in the chapter's format:
> > #     five lines per record (id, first name, last name, class code, GPA).
> > class StudentTextFileWriter(StudentWriter):
> >     def __init__(self, outputSrc):
> >         self._outputSrc = outputSrc
> >         self._outputFile = None
> >
> >     def open(self):
> >         self._outputFile = open(self._outputSrc, "w")
> >
> >     def writeRecord(self, record):
> >         assert self._outputFile is not None, "The writer is not open."
> >         self._outputFile.write(f"{record.idNum}\n{record.firstName}\n"
> >                                f"{record.lastName}\n{record.classCode}\n"
> >                                f"{record.gpa:.2f}\n")
> >
> >     def close(self):
> >         assert self._outputFile is not None, "The writer is not open."
> >         self._outputFile.close()
> >         self._outputFile = None
> > ```
> >
> > The program, `studentsort.py`:
> >
> > ```python
> > # studentsort.py: Project 1.5(d). Reads student records, sorts them the way
> > # the user asks, shows them on screen and also saves them to a text file.
> > from studentcsvfile import StudentFileReader
> > from studentwriter import StudentTerminalWriter, StudentTextFileWriter
> >
> >
> > def main():
> >     reader = StudentFileReader("students.csv")       # the file from Project 1.4
> >     reader.open()
> >     records = reader.fetchAll()
> >     reader.close()
> >
> >     choice = input("Sort by (1) student id or (2) name? ").strip()
> >     while choice not in ("1", "2"):
> >         choice = input("Please type 1 or 2: ").strip()
> >     if choice == "1":
> >         records.sort(key=lambda rec: rec.idNum)
> >     else:
> >         records.sort(key=lambda rec: (rec.lastName, rec.firstName))
> >
> >     # One ADT, two implementations: this loop doesn't care which one it gets.
> >     for writer in (StudentTerminalWriter(), StudentTextFileWriter("sorted_students.txt")):
> >         writer.open()
> >         writer.writeAll(records)
> >         writer.close()
> >
> >
> > if __name__ == "__main__":
> >     main()
> > ```
> >
> > **Check.** Output of `python studentsort.py` with `2` (sort by name) as the input. The input was piped in, so it doesn't appear after the prompt:
> >
> > ```text
> > Sort by (1) student id or (2) name? 
> >                  LIST OF STUDENTS
> > ID     NAME                       CLASS        GPA
> > -----  -------------------------  ----------  ----
> > 10333  Brooks, Lena               Freshman    2.85
> > 10512  Chen, Maya                 Sophomore   3.47
> > 10087  Haddad, Omar               Senior      3.92
> > 10204  Patel, Ravi                Junior      3.10
> > --------------------------------------------------
> > Number of students: 4
> > ```
> >
> > Contents of `sorted_students.txt`, written by the text-file writer, five lines per record:
> >
> > ```text
> > 10333
> > Lena
> > Brooks
> > 1
> > 2.85
> > 10512
> > Maya
> > Chen
> > 2
> > 3.47
> > 10087
> > Omar
> > Haddad
> > 4
> > 3.92
> > 10204
> > Ravi
> > Patel
> > 3
> > 3.10
> > ```
> >
> > Sorted by last name (Brooks, Chen, Haddad, Patel) on screen and in the file ✓
> >
> > **Insight.** Both writers share one interface, so the program's loop treats them alike. Changing where the output goes means creating a different object, not rewriting the code that uses it.

> [!example] Project 1.6 — Time ADT
> **Problem.** Implement a Time ADT that stores a time of day as the number of seconds since midnight, with these operations:
>
> | Operation | What it does |
> |---|---|
> | `Time( hours, minutes, seconds )` | a new time on the 24-hour clock |
> | `hour()`, `minutes()`, `seconds()` | one part of the time |
> | `numSeconds( otherTime )` | the seconds between this time and `otherTime`, as a positive integer |
> | `isAM()` | is it at or before 12:00:00 noon? |
> | `isPM()` | is it after noon? |
> | comparable | order two times with any comparison operator |
> | toString → `str()` | the time on the 12-hour clock, as `hh:mm:ss` |
>
> **Your attempt:** `Small Coding Projects\Time_ADT.py`
>
> > [!success]- Click to reveal solution
> > **Approach.** One integer, `_secs`, holds the seconds since midnight: the same idea as the Date's Julian day. The parts come back with `//` and `%`, and each comparison compares two integers. As the book defines it, 12:00:00 noon itself counts as AM.
> >
> > ```python
> > # timeofday.py: the Time ADT, a time of day stored as seconds since midnight
> > # (Project 1.6). Named timeofday.py because time.py would hide Python's own time module.
> > _NOON = 12 * 3600
> >
> >
> > class Time:
> >     # Creates a time on the 24-hour clock, e.g. Time(21, 45, 0).
> >     def __init__(self, hours, minutes, seconds):
> >         assert 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60, \
> >             "Invalid time."
> >         self._secs = hours * 3600 + minutes * 60 + seconds
> >
> >     # The attribute is _secs, not seconds: an attribute named like a
> >     # method would hide that method.
> >     def hour(self):
> >         return self._secs // 3600
> >
> >     def minutes(self):
> >         return self._secs // 60 % 60
> >
> >     def seconds(self):
> >         return self._secs % 60
> >
> >     def numSeconds(self, otherTime):
> >         return abs(self._secs - otherTime._secs)
> >
> >     # The book counts 12:00:00 noon itself as AM.
> >     def isAM(self):
> >         return self._secs <= _NOON
> >
> >     def isPM(self):
> >         return self._secs > _NOON
> >
> >     def __eq__(self, otherTime):
> >         return self._secs == otherTime._secs
> >
> >     def __lt__(self, otherTime):
> >         return self._secs < otherTime._secs
> >
> >     def __le__(self, otherTime):
> >         return self._secs <= otherTime._secs
> >
> >     # 12-hour clock: hour 0 shows as 12, hour 13 as 1, and so on.
> >     def __str__(self):
> >         hour12 = self.hour() % 12
> >         if hour12 == 0:
> >             hour12 = 12
> >         return f"{hour12:02d}:{self.minutes():02d}:{self.seconds():02d}"
> >
> >
> > if __name__ == "__main__":
> >     morning, noon, evening = Time(9, 5, 30), Time(12, 0, 0), Time(21, 45, 0)
> >     for t in (morning, noon, evening):
> >         print(t, " hour", f"{t.hour():2d}", " isAM", f"{t.isAM()!s:<5}", " isPM", t.isPM())
> >     print("morning to evening:", morning.numSeconds(evening), "seconds")
> >     print("morning < evening:", morning < evening, " evening >= noon:", evening >= noon)
> >     print("midnight shows as", Time(0, 0, 0))
> > ```
> >
> > **Check.** Output of `python timeofday.py`:
> >
> > ```text
> > 09:05:30  hour  9  isAM True   isPM False
> > 12:00:00  hour 12  isAM True   isPM False
> > 09:45:00  hour 21  isAM False  isPM True
> > morning to evening: 45570 seconds
> > morning < evening: True  evening >= noon: True
> > midnight shows as 12:00:00
> > ```
> >
> > 9:05:30 to 21:45:00 is 12 h 39 min 30 s = 45,570 seconds ✓
> >
> > **Insight.** One number as the storage makes `numSeconds` and the comparisons one line each. Watch the naming trap the comment mentions: writing `self.seconds = seconds` in `__init__` would hide the method `seconds()` on that object.

> [!example] Project 1.7 — TimeDate ADT
> **Problem.** Design and implement a TimeDate ADT that holds a date and a time of day together as a single value.
>
> > [!success]- Click to reveal solution
> > **Approach.** Reuse the two ADTs already built: a TimeDate holds a `Date` and a `Time` (Project 1.6) and calls only their public operations. `advanceBy()` adds the seconds to the time of day and lets `divmod` carry whole days over into the date. Design:
> >
> > | Operation | What it does |
> > |---|---|
> > | `TimeDate( month, day, year, hours = 0, minutes = 0, seconds = 0 )` | a new date and time; both parts must be valid |
> > | `date()`, `time()` | the `Date` part and the `Time` part |
> > | `advanceBy( seconds )` | move forward or back; passing midnight changes the date |
> > | `numSeconds( other )` | the seconds between the two, as a positive integer |
> > | comparable | earlier date first; on the same date, earlier time first |
> > | toString → `str()` | `mm/dd/yyyy hh:mm:ss` on the 24-hour clock |
> >
> > ```python
> > # timedate.py: the TimeDate ADT, a date and a time of day as one value (Project 1.7).
> > from date import Date
> > from timeofday import Time
> >
> > _MIDNIGHT = Time(0, 0, 0)
> > _SECONDS_PER_DAY = 24 * 3600
> >
> >
> > # Seconds since midnight, using only Time's public operations.
> > def _secondsOf(time):
> >     return time.numSeconds(_MIDNIGHT)
> >
> >
> > class TimeDate:
> >     # Each part checks its own preconditions in its own constructor.
> >     def __init__(self, month, day, year, hours=0, minutes=0, seconds=0):
> >         self._date = Date(month, day, year)
> >         self._time = Time(hours, minutes, seconds)
> >
> >     # A copy, so the caller can't move our date with advanceBy().
> >     def date(self):
> >         return Date(self._date.month(), self._date.day(), self._date.year())
> >
> >     # Time has no operation that changes it, so sharing it is safe.
> >     def time(self):
> >         return self._time
> >
> >     # Moves forward (seconds > 0) or back (seconds < 0). divmod splits the
> >     # total into whole days and leftover seconds; it rounds down, so a
> >     # negative total borrows a day correctly.
> >     def advanceBy(self, seconds):
> >         days, secs = divmod(_secondsOf(self._time) + seconds, _SECONDS_PER_DAY)
> >         self._date.advanceBy(days)
> >         self._time = Time(secs // 3600, secs // 60 % 60, secs % 60)
> >
> >     def numSeconds(self, other):
> >         days = self._date.numDays(other._date)
> >         if self._date < other._date:
> >             days = -days
> >         return abs(days * _SECONDS_PER_DAY
> >                    + _secondsOf(self._time) - _secondsOf(other._time))
> >
> >     # Tuples compare item by item: the dates first, the times only on a tie.
> >     def __eq__(self, other):
> >         return (self._date, self._time) == (other._date, other._time)
> >
> >     def __lt__(self, other):
> >         return (self._date, self._time) < (other._date, other._time)
> >
> >     def __le__(self, other):
> >         return (self._date, self._time) <= (other._date, other._time)
> >
> >     # 24-hour clock here, so the text is never ambiguous.
> >     def __str__(self):
> >         t = self._time
> >         return f"{self._date} {t.hour():02d}:{t.minutes():02d}:{t.seconds():02d}"
> >
> >
> > if __name__ == "__main__":
> >     moment = TimeDate(12, 31, 2025, 23, 59, 30)
> >     print("start:      ", moment)
> >     moment.advanceBy(45)
> >     print("+45 seconds:", moment)
> >     moment.advanceBy(-3600)
> >     print("-1 hour:    ", moment)
> >     noon = TimeDate(1, 1, 2026, 12)
> >     print("seconds until", noon, "->", moment.numSeconds(noon))
> >     print("moment < noon:", moment < noon, " moment == noon:", moment == noon)
> >     print("noon.date():", noon.date(), " noon.time() in 12-hour form:", noon.time())
> > ```
> >
> > **Check.** Output of `python timedate.py`:
> >
> > ```text
> > start:       12/31/2025 23:59:30
> > +45 seconds: 01/01/2026 00:00:15
> > -1 hour:     12/31/2025 23:00:15
> > seconds until 01/01/2026 12:00:00 -> 46785
> > moment < noon: True  moment == noon: False
> > noon.date(): 01/01/2026  noon.time() in 12-hour form: 12:00:00
> > ```
> >
> > Midnight is crossed correctly in both directions, and from 23:00:15 to noon the next day is 59 min 45 s + 12 h = 46,785 seconds ✓
> >
> > **Insight.** Building a new ADT out of existing ones gives you their preconditions and conversions for free: a bad date or time is rejected by its own constructor. `str()` uses the 24-hour clock because the Time ADT's 12-hour string has no AM/PM and would be ambiguous here.

> [!example] Project 1.8 — Line Segment ADT
> **Problem.** Implement a Line Segment ADT: a straight segment between two endpoints on the x-y plane. The book builds it on the `Point` class from its Appendix D. Operations:
> - `LineSegment( ptA, ptB )`: a segment between two `Point` objects
> - `endPointA()`, `endPointB()`: the endpoints
> - `length()`: the Euclidean distance between the endpoints
> - toString → `str()`: the format `(Ax, Ay)#(Bx, By)`
> - `isVertical()`, `isHorizontal()`: parallel to the y-axis? to the x-axis?
> - `isParallel( otherLine )`, `isPerpendicular( otherLine )`
> - `intersects( otherLine )`, `bisects( otherLine )`
> - `slope()`: rise over run, or `None` for a vertical segment
> - `shift( xInc, yInc )`: move by `xInc` along x and `yInc` along y
> - `midpoint()`: the middle, as a `Point`
>
> **Your attempt:** `Small Coding Projects\Line_Segment_ADT.py`
>
> > [!success]- Click to reveal solution
> > **Approach.** Appendix D isn't covered here, so `point.py` defines a minimal `Point`. Definitions used: `intersects` is true when the segments cross **or touch** (an endpoint counts), tested with orientation (cross-product) checks; `bisects` is true when this segment passes through the other segment's midpoint. Parallel and perpendicular compare direction vectors, so vertical segments need no special case; only `slope()` returns `None` for them.
> >
> > ```python
> > # point.py: a minimal 2-D point, standing in for the book's Appendix D class.
> > import math
> >
> >
> > class Point:
> >     def __init__(self, x, y):
> >         self._x = x
> >         self._y = y
> >
> >     def getX(self):
> >         return self._x
> >
> >     def getY(self):
> >         return self._y
> >
> >     def distance(self, otherPoint):
> >         return math.hypot(self._x - otherPoint._x, self._y - otherPoint._y)
> >
> >     def __eq__(self, otherPoint):
> >         return self._x == otherPoint._x and self._y == otherPoint._y
> >
> >     def __str__(self):
> >         return f"({self._x}, {self._y})"
> > ```
> >
> > ```python
> > # linesegment.py: the Line Segment ADT (Project 1.8).
> > from point import Point
> >
> > _EPSILON = 1e-9         # floats are rarely exactly 0, so treat tiny values as 0
> >
> >
> > # Which way does the path p -> q -> r turn? +1 left, -1 right, 0 straight
> > # (all three points on one line). It is the sign of a cross product.
> > def _orientation(p, q, r):
> >     cross = ((q.getX() - p.getX()) * (r.getY() - p.getY())
> >              - (q.getY() - p.getY()) * (r.getX() - p.getX()))
> >     if abs(cross) < _EPSILON:
> >         return 0
> >     return 1 if cross > 0 else -1
> >
> >
> > # For r already on the line through p and q: is r between p and q?
> > def _onSegment(p, q, r):
> >     return (min(p.getX(), q.getX()) <= r.getX() <= max(p.getX(), q.getX()) and
> >             min(p.getY(), q.getY()) <= r.getY() <= max(p.getY(), q.getY()))
> >
> >
> > class LineSegment:
> >     def __init__(self, ptA, ptB):
> >         assert ptA != ptB, "The two endpoints must differ."
> >         self._ptA = ptA          # Points never change, so keeping the
> >         self._ptB = ptB          # caller's objects is safe
> >
> >     def endPointA(self):
> >         return self._ptA
> >
> >     def endPointB(self):
> >         return self._ptB
> >
> >     def length(self):
> >         return self._ptA.distance(self._ptB)
> >
> >     def __str__(self):
> >         return f"{self._ptA}#{self._ptB}"
> >
> >     # Run and rise: how far the segment goes along x and along y.
> >     def _dx(self):
> >         return self._ptB.getX() - self._ptA.getX()
> >
> >     def _dy(self):
> >         return self._ptB.getY() - self._ptA.getY()
> >
> >     def isVertical(self):
> >         return abs(self._dx()) < _EPSILON
> >
> >     def isHorizontal(self):
> >         return abs(self._dy()) < _EPSILON
> >
> >     # Direction vectors instead of slopes, so vertical segments need no special case.
> >     def isParallel(self, otherLine):
> >         return abs(self._dx() * otherLine._dy() - self._dy() * otherLine._dx()) < _EPSILON
> >
> >     def isPerpendicular(self, otherLine):
> >         return abs(self._dx() * otherLine._dx() + self._dy() * otherLine._dy()) < _EPSILON
> >
> >     # True if the segments cross or touch (an endpoint counts).
> >     def intersects(self, otherLine):
> >         a, b = self._ptA, self._ptB
> >         c, d = otherLine._ptA, otherLine._ptB
> >         o1, o2 = _orientation(a, b, c), _orientation(a, b, d)
> >         o3, o4 = _orientation(c, d, a), _orientation(c, d, b)
> >         if o1 != o2 and o3 != o4:            # each segment has the other's ends on both sides
> >             return True
> >         # Otherwise they meet only if an endpoint lies on the other segment.
> >         return ((o1 == 0 and _onSegment(a, b, c)) or (o2 == 0 and _onSegment(a, b, d)) or
> >                 (o3 == 0 and _onSegment(c, d, a)) or (o4 == 0 and _onSegment(c, d, b)))
> >
> >     # True if this segment passes through the other segment's midpoint.
> >     def bisects(self, otherLine):
> >         mid = otherLine.midpoint()
> >         return _orientation(self._ptA, self._ptB, mid) == 0 and _onSegment(self._ptA, self._ptB, mid)
> >
> >     def slope(self):
> >         if self.isVertical():
> >             return None
> >         return self._dy() / self._dx()
> >
> >     def shift(self, xInc, yInc):
> >         self._ptA = Point(self._ptA.getX() + xInc, self._ptA.getY() + yInc)
> >         self._ptB = Point(self._ptB.getX() + xInc, self._ptB.getY() + yInc)
> >
> >     def midpoint(self):
> >         return Point((self._ptA.getX() + self._ptB.getX()) / 2,
> >                      (self._ptA.getY() + self._ptB.getY()) / 2)
> >
> >
> > if __name__ == "__main__":
> >     a = LineSegment(Point(0, 0), Point(4, 4))
> >     b = LineSegment(Point(0, 4), Point(4, 0))
> >     print("a =", a, " length", round(a.length(), 4), " slope", a.slope(), " midpoint", a.midpoint())
> >     print("a and b: intersect", a.intersects(b), " perpendicular", a.isPerpendicular(b),
> >           " a bisects b", a.bisects(b))
> >     c = LineSegment(Point(0, 0), Point(4, 0))
> >     d = LineSegment(Point(5, 0), Point(9, 0))       # same line, but past c's end
> >     e = LineSegment(Point(4, 0), Point(4, 3))       # touches c at (4, 0)
> >     print("c and d: parallel", c.isParallel(d), " intersect", c.intersects(d))
> >     print("c and e: intersect", c.intersects(e), " c bisects e", c.bisects(e))
> >     print("e: vertical", e.isVertical(), " horizontal", e.isHorizontal(),
> >           " slope", e.slope(), " length", e.length())
> >     e.shift(-2, -1.5)
> >     print("e shifted by (-2, -1.5):", e, " c bisects e", c.bisects(e), " e bisects c", e.bisects(c))
> > ```
> >
> > **Check.** Output of `python linesegment.py`:
> >
> > ```text
> > a = (0, 0)#(4, 4)  length 5.6569  slope 1.0  midpoint (2.0, 2.0)
> > a and b: intersect True  perpendicular True  a bisects b True
> > c and d: parallel True  intersect False
> > c and e: intersect True  c bisects e False
> > e: vertical True  horizontal False  slope None  length 3.0
> > e shifted by (-2, -1.5): (2, -1.5)#(2, 1.5)  c bisects e True  e bisects c True
> > ```
> >
> > The diagonals of a square cross at right angles and bisect each other; c and d lie on one line but don't overlap; e touches c only at (4, 0); after the shift, c and e bisect each other ✓
> >
> > **Insight.** Orientation tests avoid slopes, which break on vertical lines. The small tolerance `_EPSILON` stops float noise (like `0.30000000000000004`) from flipping a yes/no answer.

> [!example] Project 1.9 — Polygon ADT
> **Problem.** A polygon is a closed shape made of three or more line segments joined end to end; the joints are its vertices, given as points on the x-y plane. (a) Define a Polygon ADT with a sensible set of operations. (b) Implement it in Python.
>
> > [!success]- Click to reveal solution
> > **Approach.** A list of `Point`s, because a polygon's vertices have an order (a bag's items don't). The sides are built when asked for, as `LineSegment`s from Project 1.8. Design:
> >
> > | Operation | What it does |
> > |---|---|
> > | `Polygon( vertices )` | a polygon from a list of 3 or more `Point`s, in order around the shape |
> > | length → `len()` | the number of vertices (the same as the number of sides) |
> > | `vertex( i )` | the vertex at index `i` |
> > | iterator → `for v in p` | visit the vertices in order |
> > | `sides()` | the sides, as a list of `LineSegment` objects |
> > | `perimeter()` | the total length of the sides |
> > | `area()` | the area inside (shoelace formula; sides must not cross) |
> > | `isConvex()` | do all corners turn the same way? |
> > | toString → `str()` | `(x, y) -> (x, y) -> …` |
> >
> > ```python
> > # polygon.py: the Polygon ADT (Project 1.9). The vertices are kept in a
> > # list, in order around the shape; side i joins vertex i to vertex i + 1.
> > from point import Point
> > from linesegment import LineSegment
> >
> >
> > class Polygon:
> >     def __init__(self, vertices):
> >         assert len(vertices) >= 3, "A polygon needs at least 3 vertices."
> >         self._vertices = list(vertices)        # our own copy of the list
> >
> >     def __len__(self):
> >         return len(self._vertices)
> >
> >     def vertex(self, i):
> >         assert 0 <= i < len(self._vertices), "Vertex index out of range."
> >         return self._vertices[i]
> >
> >     def __iter__(self):
> >         return iter(self._vertices)
> >
> >     # The last side wraps around: % n turns index n back into 0.
> >     def sides(self):
> >         n = len(self._vertices)
> >         return [LineSegment(self._vertices[i], self._vertices[(i + 1) % n])
> >                 for i in range(n)]
> >
> >     def perimeter(self):
> >         return sum(side.length() for side in self.sides())
> >
> >     # Shoelace formula: add x1*y2 - x2*y1 for every side, halve, drop the sign.
> >     # Valid for simple polygons (sides that don't cross each other).
> >     def area(self):
> >         total = 0
> >         for side in self.sides():
> >             p, q = side.endPointA(), side.endPointB()
> >             total += p.getX() * q.getY() - q.getX() * p.getY()
> >         return abs(total) / 2
> >
> >     # Convex: every corner turns the same way (all left or all right).
> >     def isConvex(self):
> >         turns = set()
> >         n = len(self._vertices)
> >         for i in range(n):
> >             a, b, c = self._vertices[i], self._vertices[(i + 1) % n], self._vertices[(i + 2) % n]
> >             cross = ((b.getX() - a.getX()) * (c.getY() - b.getY())
> >                      - (b.getY() - a.getY()) * (c.getX() - b.getX()))
> >             if cross != 0:                     # skip straight corners
> >                 turns.add(cross > 0)           # True = left turn, False = right turn
> >         return len(turns) <= 1
> >
> >     def __str__(self):
> >         return " -> ".join(str(p) for p in self)
> >
> >
> > if __name__ == "__main__":
> >     rect = Polygon([Point(0, 0), Point(4, 0), Point(4, 3), Point(0, 3)])
> >     print("rectangle:", rect)
> >     print("  vertices", len(rect), " perimeter", rect.perimeter(),
> >           " area", rect.area(), " convex", rect.isConvex(), " vertex(2)", rect.vertex(2))
> >     dart = Polygon([Point(0, 0), Point(4, 2), Point(0, 4), Point(1, 2)])
> >     print("dart:", dart)
> >     print("  vertices", len(dart), " perimeter", round(dart.perimeter(), 4),
> >           " area", dart.area(), " convex", dart.isConvex())
> >     print("  sides:", ", ".join(str(side) for side in dart.sides()))
> > ```
> >
> > **Check.** Output of `python polygon.py`:
> >
> > ```text
> > rectangle: (0, 0) -> (4, 0) -> (4, 3) -> (0, 3)
> >   vertices 4  perimeter 14.0  area 12.0  convex True  vertex(2) (4, 3)
> > dart: (0, 0) -> (4, 2) -> (0, 4) -> (1, 2)
> >   vertices 4  perimeter 13.4164  area 6.0  convex False
> >   sides: (0, 0)#(4, 2), (4, 2)#(0, 4), (0, 4)#(1, 2), (1, 2)#(0, 0)
> > ```
> >
> > The 4 × 3 rectangle has perimeter 14 and area 12. The dart (an arrowhead) has area 6 and one corner that turns the other way, so it isn't convex ✓
> >
> > **Insight.** Choosing an ADT's operations is part of the design: here they are the questions people ask about a shape. Reusing `LineSegment` means `perimeter()` is just a sum of `length()` calls.

> [!example] Project 1.10 — Activities Calendar ADT
> **Problem.** Choose a data structure and implement this ADT, which keeps at most one activity per day over a range of dates:
> - `ActivitiesCalendar( dateFrom, dateTo )`: an empty calendar for that range. `dateFrom` must come before `dateTo`, and the range must end before `dateFrom`'s month and day come round again the next year.
> - length → `len()`: how many activities are on the calendar
> - `getActivity( date )`: the description of the activity on `date`, or `None` if there isn't one
> - `addActivity( date, activity )`: put an activity on `date`, which must be inside the range
> - `displayMonth( month )`: print the month's name and year, then each activity in that month with its day of the month
>
> **Your attempt:** `Small Coding Projects\Date ADT\Activity_Calendar.py`
>
> > [!success]- Click to reveal solution
> > **Approach.** Data structure: a dictionary keyed by the number of days since `dateFrom` (worked out with the public `numDays()`), with the description as the value. It holds only the days that have an activity, finds any day in one step, and its `len()` is the number of activities. `displayMonth()` walks the range day by day, so a range that meets the same month in two years (August 2026 and August 2027 below) gets a heading for each.
> >
> > ```python
> > # activities.py: the Activities Calendar ADT (Project 1.10).
> > # Data structure: a dict keyed by "days since dateFrom". It holds only the days
> > # that have an activity, finds any day in one step, and its len() is the count.
> > from date import Date
> >
> >
> > # Our own copy of a Date, so the caller can't move our dates with advanceBy().
> > def _copy(date):
> >     return Date(date.month(), date.day(), date.year())
> >
> >
> > class ActivitiesCalendar:
> >     def __init__(self, dateFrom, dateTo):
> >         assert dateFrom < dateTo, "dateFrom must come before dateTo."
> >         # The range must end before dateFrom's month and day come round again.
> >         sameYear = dateTo.year() == dateFrom.year()
> >         nextYearEarlier = (dateTo.year() == dateFrom.year() + 1 and
> >                            (dateTo.month(), dateTo.day()) < (dateFrom.month(), dateFrom.day()))
> >         assert sameYear or nextYearEarlier, "The range may not reach the same day next year."
> >         self._dateFrom = _copy(dateFrom)
> >         self._dateTo = _copy(dateTo)
> >         self._activities = dict()          # days since dateFrom -> description
> >
> >     def __len__(self):
> >         return len(self._activities)
> >
> >     def _inRange(self, date):
> >         return self._dateFrom <= date <= self._dateTo
> >
> >     def getActivity(self, date):
> >         if not self._inRange(date):
> >             return None
> >         return self._activities.get(self._dateFrom.numDays(date))
> >
> >     def addActivity(self, date, activity):
> >         assert self._inRange(date), "The date is outside the calendar's range."
> >         self._activities[self._dateFrom.numDays(date)] = activity
> >
> >     # Walks the range one day at a time. A range that starts mid-month can
> >     # meet the same month twice (August 2026 and August 2027), so a new
> >     # heading is printed whenever the year changes.
> >     def displayMonth(self, month):
> >         assert 1 <= month <= 12, "Invalid month."
> >         day = _copy(self._dateFrom)
> >         shownYear = None
> >         while day <= self._dateTo:
> >             if day.month() == month:
> >                 if day.year() != shownYear:
> >                     shownYear = day.year()
> >                     print(f"{day.monthName()} {shownYear}")
> >                 activity = self.getActivity(day)
> >                 if activity is not None:
> >                     print(f"  {day.day():2d}  {activity}")
> >             day.advanceBy(1)
> >
> >
> > if __name__ == "__main__":
> >     school = ActivitiesCalendar(Date(8, 24, 2026), Date(8, 20, 2027))
> >     school.addActivity(Date(8, 24, 2026), "Fall classes begin")
> >     school.addActivity(Date(8, 28, 2026), "Welcome picnic")
> >     school.addActivity(Date(10, 30, 2026), "Halloween concert")
> >     school.addActivity(Date(8, 13, 2027), "Summer graduation")
> >     print("activities:", len(school))
> >     print("10/30/2026:", school.getActivity(Date(10, 30, 2026)))
> >     print("10/31/2026:", school.getActivity(Date(10, 31, 2026)))
> >     school.displayMonth(8)
> >     school.displayMonth(10)
> >     try:
> >         school.addActivity(Date(9, 1, 2027), "Too late")
> >     except AssertionError as error:
> >         print("09/01/2027 ->", error)
> >     try:
> >         ActivitiesCalendar(Date(8, 24, 2026), Date(8, 24, 2027))
> >     except AssertionError as error:
> >         print("08/24/2026 to 08/24/2027 ->", error)
> > ```
> >
> > **Check.** Output of `python activities.py`:
> >
> > ```text
> > activities: 4
> > 10/30/2026: Halloween concert
> > 10/31/2026: None
> > August 2026
> >   24  Fall classes begin
> >   28  Welcome picnic
> > August 2027
> >   13  Summer graduation
> > October 2026
> >   30  Halloween concert
> > 09/01/2027 -> The date is outside the calendar's range.
> > 08/24/2026 to 08/24/2027 -> The range may not reach the same day next year.
> > ```
> >
> > **Insight.** The key works like a private Julian day for the calendar, but it is built from `Date`'s public operations, so the calendar never reaches into `_julianDay`. Keeping copies of `dateFrom` and `dateTo` stops a caller from changing the range later with `advanceBy()`.

> [!example] Project 1.11 — Fraction ADT
> **Problem.** Floats are stored in binary, so most real numbers can't be stored exactly. A fraction (an integer numerator over an integer denominator greater than zero) can be exact. (a) Define a Fraction ADT with the usual arithmetic and comparison operations, conversion between floats and fractions, and a string form. (b) Implement it.
>
> > [!success]- Click to reveal solution
> > **Approach.** Two integers, always kept in lowest terms with the sign in the numerator, so equal fractions have identical fields. `fromFloat` uses `as_integer_ratio()`, which gives a float's exact binary value; with `maxDenominator` it walks that value's continued fraction and stops at the last convergent whose denominator fits. (Python's own `fractions.Fraction.limit_denominator` also tries in-between candidates, so it is sometimes closer: with a limit of 100, pi gives 22/7 here and 311/99 there.) Design:
> >
> > | Operation | Python form | What it does |
> > |---|---|---|
> > | `Fraction( numerator, denominator = 1 )` | `Fraction(7, 8)` | a new fraction in lowest terms; the denominator can't be 0 |
> > | `numerator()`, `denominator()` | | the two parts |
> > | add, subtract, multiply, divide | `+ - * /` | a new fraction; an `int` also works on the right |
> > | negate | `-f` | the same fraction with the opposite sign |
> > | comparable | `== != < <= > >=` | exact ordering |
> > | toFloat | `float(f)` | the nearest float |
> > | `fromFloat( value, maxDenominator = None )` | `Fraction.fromFloat(0.75)` | float → fraction, exact or limited |
> > | toString | `str(f)` | `7/8`, or `3` for a whole number |
> >
> > ```python
> > # fraction.py: the Fraction ADT, an exact rational number (Project 1.11).
> > import math
> >
> >
> > class Fraction:
> >     # Creates numerator/denominator, kept in lowest terms with the sign on top.
> >     def __init__(self, numerator, denominator=1):
> >         assert isinstance(numerator, int) and isinstance(denominator, int), \
> >             "The numerator and denominator must be integers."
> >         assert denominator != 0, "The denominator cannot be zero."
> >         if denominator < 0:
> >             numerator, denominator = -numerator, -denominator
> >         common = math.gcd(numerator, denominator)     # gcd(0, 5) is 5, so 0/5 -> 0/1
> >         self._num = numerator // common
> >         self._den = denominator // common
> >
> >     def numerator(self):
> >         return self._num
> >
> >     def denominator(self):
> >         return self._den
> >
> >     # Arithmetic. Every result goes through the constructor, which reduces it.
> >     def __add__(self, other):
> >         other = _asFraction(other)
> >         return Fraction(self._num * other._den + other._num * self._den,
> >                         self._den * other._den)
> >
> >     def __sub__(self, other):
> >         return self + (-_asFraction(other))
> >
> >     def __mul__(self, other):
> >         other = _asFraction(other)
> >         return Fraction(self._num * other._num, self._den * other._den)
> >
> >     def __truediv__(self, other):
> >         other = _asFraction(other)
> >         assert other._num != 0, "Cannot divide by zero."
> >         return Fraction(self._num * other._den, self._den * other._num)
> >
> >     def __neg__(self):
> >         return Fraction(-self._num, self._den)
> >
> >     # Lowest terms make equal fractions look identical. For order,
> >     # a/b < c/d exactly when a*d < c*b, because b and d are positive.
> >     def __eq__(self, other):
> >         other = _asFraction(other)
> >         return self._num == other._num and self._den == other._den
> >
> >     def __lt__(self, other):
> >         other = _asFraction(other)
> >         return self._num * other._den < other._num * self._den
> >
> >     def __le__(self, other):
> >         other = _asFraction(other)
> >         return self._num * other._den <= other._num * self._den
> >
> >     def __float__(self):
> >         return self._num / self._den
> >
> >     # Float -> Fraction. Without a limit you get the float's exact binary value.
> >     # With maxDenominator you get the last convergent of its continued fraction
> >     # whose denominator fits: the closest such convergent, e.g. 0.1 -> 1/10.
> >     @staticmethod
> >     def fromFloat(value, maxDenominator=None):
> >         num, den = value.as_integer_ratio()
> >         if maxDenominator is None:
> >             return Fraction(num, den)
> >         assert maxDenominator >= 1, "maxDenominator must be at least 1."
> >         p0, q0, p1, q1 = 0, 1, 1, 0              # the two previous convergents
> >         while den != 0:
> >             whole, rest = divmod(num, den)
> >             p0, q0, p1, q1 = p1, q1, whole * p1 + p0, whole * q1 + q0
> >             if q1 > maxDenominator:
> >                 return Fraction(p0, q0)
> >             num, den = den, rest
> >         return Fraction(p1, q1)
> >
> >     def __str__(self):
> >         if self._den == 1:
> >             return str(self._num)
> >         return f"{self._num}/{self._den}"
> >
> >
> > # Lets plain ints mix with fractions, e.g. Fraction(1, 2) + 1.
> > def _asFraction(value):
> >     if isinstance(value, int):
> >         return Fraction(value)
> >     assert isinstance(value, Fraction), "Expected a Fraction or an int."
> >     return value
> >
> >
> > if __name__ == "__main__":
> >     half, third = Fraction(1, 2), Fraction(1, 3)
> >     print("1/2 + 1/3 =", half + third, "  1/2 - 1/3 =", half - third,
> >           "  1/2 * 1/3 =", half * third, "  1/2 / 1/3 =", half / third)
> >     print("Fraction(6, -8) =", Fraction(6, -8), "  Fraction(1, 2) + 1 =", half + 1,
> >           "  Fraction(10, 5) =", Fraction(10, 5))
> >     print("3/4 < 4/5:", Fraction(3, 4) < Fraction(4, 5), "  2/4 == 1/2:", Fraction(2, 4) == half,
> >           "  1/3 >= 1/2:", third >= half)
> >     print("float(7/8) =", float(Fraction(7, 8)))
> >     print("fromFloat(0.75)       =", Fraction.fromFloat(0.75))
> >     print("fromFloat(0.1)        =", Fraction.fromFloat(0.1))
> >     print("fromFloat(0.1, 1000)  =", Fraction.fromFloat(0.1, 1000))
> >     print("fromFloat(pi, 1000)   =", Fraction.fromFloat(math.pi, 1000))
> >     print("0.1 + 0.2 == 0.3 with floats:", 0.1 + 0.2 == 0.3,
> >           "  with fractions:", Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
> > ```
> >
> > **Check.** Output of `python fraction.py`:
> >
> > ```text
> > 1/2 + 1/3 = 5/6   1/2 - 1/3 = 1/6   1/2 * 1/3 = 1/6   1/2 / 1/3 = 3/2
> > Fraction(6, -8) = -3/4   Fraction(1, 2) + 1 = 3/2   Fraction(10, 5) = 2
> > 3/4 < 4/5: True   2/4 == 1/2: True   1/3 >= 1/2: False
> > float(7/8) = 0.875
> > fromFloat(0.75)       = 3/4
> > fromFloat(0.1)        = 3602879701896397/36028797018963968
> > fromFloat(0.1, 1000)  = 1/10
> > fromFloat(pi, 1000)   = 355/113
> > 0.1 + 0.2 == 0.3 with floats: False   with fractions: True
> > ```
> >
> > The last line is the reason this ADT exists: with floats, 0.1 + 0.2 isn't 0.3, but with fractions it is ✓
> >
> > **Insight.** Keeping the data normalized (a rule the constructor enforces every time) makes every other operation simpler: `==` compares two pairs of integers, and `<` can cross-multiply without worrying about signs.

---

## Related Documents

- **[Chapter 1 — Abstract Data Types](<Chapter 1 (Main).md>)** — the chapter notes these exercises practise.
- **[Abstract Data Types, first-pass summary](<Abstract Data Types (DSA Ch. 1).md>)** — the earlier summary, with the book's listings.
- **[Data Structures and Algorithms Using Python](<Data Structures and Algorithms Using Python (Main).md>)** — the book's overview.
