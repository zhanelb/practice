#1
from datetime import datetime, timedelta
currentdate=datetime.now()
newdate=currentdate - timedelta(days=5)
print("Current date:", currentdate)
print("5 days ago:", newdate)
#2
from datetime import datetime, timedelta
currentdate=datetime.now()
tomorrow=currentdate + timedelta(days=1)
yesterday=currentdate - timedelta(days=1)
print("yesterday", yesterday)
print("today", currentdate)
print("tomorrow:", tomorrow)
#3
from datetime import datetime, timedelta
now=datetime.now()
without=now.replace(microsecond=0)
print("With microseconds:", now)
print("With out microseconds:", without)
#4
from datetime import datetime
date1 = datetime(2026, 1, 1)
date2 = datetime(2026, 2, 1)
diff= date2 - date1
print("Difference in seconds:", diff.total_seconds())
