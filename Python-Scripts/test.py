import os
from datetime import datetime,timedelta

def get_tomorrow(date):
    date_object = datetime.strptime(date, '%d%m%y')
    tomorrow = date_object + timedelta(days=1)
    return tomorrow.strftime('%d%m%y')


rs_path = "C:/DDA/station/data/RS050524.D1A"
date = rs_path[-10:-4]
next_rs = rs_path[:-10] + get_tomorrow(date) + rs_path[-4:]
print(next_rs)