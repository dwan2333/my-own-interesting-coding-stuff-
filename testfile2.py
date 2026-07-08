from datetime import date, time, datetime, timedelta

# July 7 2026 to December 25 2026

dt = datetime.strptime("July 7 2026", "%B %d %Y")

end_dt = datetime.strptime("December 25 2026", "%B %d %Y")

print(dt)
print(f"Start date: {dt.date()}")
print(f"End date: {end_dt.date()}")
print(f"Days between: {(end_dt - dt).days} days")


dt = date.strptime('January 1 2000', "%B %A %Y")
print(dt.weekday())
