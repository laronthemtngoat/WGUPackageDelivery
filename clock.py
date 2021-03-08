import time
from datetime import datetime
import datetime as dt


# clock class to create an adjustable 24 hour clock (can set start/end times of drivers shifts)
class Clock:
    def __init__(self, hours, minutes):
        self.start_time = dt.timedelta(hours=hours, minutes=minutes)
        self.end_time = dt.timedelta(hours=11, minutes=59)

        # sets current time to start time
        self.curr_time = self.start_time

# add time with each package delivery
    def add_delivery_time(self, add_time):
        d = dt.timedelta(minutes=add_time)
        self.curr_time += d

