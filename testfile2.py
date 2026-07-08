from datetime import datetime
d = datetime.strptime('2026-12-25', '%Y-%m-%d')
print(d.strftime('%B %d, %Y'))
print(d)
