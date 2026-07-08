# Problem. Starting from 2026-07-07 09:00:00, what date and time is it 90 days and 12 hours later?
from datetime import date, datetime


def is_leapyear(year):
    try:
        time = date(year,2,29)
        return (f'{time} is a leap year')
    except ValueError:
        return (f'{year} is not a leap year')

print(is_leapyear(2004))
