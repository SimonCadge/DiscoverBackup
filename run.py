import datetime
import discover

day = datetime.date.today().weekday()
#Check whether it's a friday.
if day == 5:
    discover.backup()