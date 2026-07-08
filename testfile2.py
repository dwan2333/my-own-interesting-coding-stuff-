from datetime import datetime 

birth = datetime(2004,1,15,19,3)

time_now = datetime.now()

print((birth - time_now).days/365)

