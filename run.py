import datetime
import discover

day = datetime.date.today().weekday()
if day == 5:
    discover.backup()