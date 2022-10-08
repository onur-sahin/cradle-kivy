from time import sleep
from datetime import datetime, timedelta

a = datetime.utcnow()
sleep(2)
b =  datetime.fromisoformat('2022-11-04 00:05:23.283')
print(a)
print(b)
print(b-a > timedelta(days=26))
