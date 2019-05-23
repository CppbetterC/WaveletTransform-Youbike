import numpy as np
import datetime
from dateutil.rrule import rrule, DAILY, MONTHLY

year = 2015
first_week = datetime.datetime.strptime(str(year) + '-' + '01' + '-' + '01', '%Y-%m-%d').weekday()
print(first_week)


start_year = 2015
end_year = 2016
target_timestamp = {}
iterval = [x for x in range(start_year, end_year, 1)]
tmp = np.array([])
for year in iterval:
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 12, 31)
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        tmp = np.append(tmp, dt.strftime("%Y-%m-%d"))

cnt = 0
print('第'+str(cnt)+'週 -> ', end=' ')
for i in range(len(tmp)):
    if i % 7 == 3:
        print()
        cnt += 1
        print('第'+str(cnt)+'週 -> ', end=' ')

    print(tmp[i], end=' ')
