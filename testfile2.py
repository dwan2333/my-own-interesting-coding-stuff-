# Problem. Starting from 2026-07-07 09:00:00, what date and time is it 90 days and 12 hours later?
from datetime import date, datetime

def is_leapyear(year):
    time = date(year,2,29)

time = date(int(input('select a year')),2,29)   
