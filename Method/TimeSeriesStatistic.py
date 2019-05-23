import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from ast import literal_eval as make_tuple

from Method.LoadData import LoadData
from Method.Export import Export


class TimeSeriesStatistic:

    def __init__(self, file):
        """
        self.station_type, 場地名稱
        self.file_name, 資料夾存在的csv檔案名稱
        """
        desired_width = 320
        pd.set_option('display.width', desired_width)
        pd.set_option('display.max_columns', 20)
        self.station = LoadData.load_refactor_ubike_station()
        self.station_type = set(self.station['sna'])
        self.file_name = file

    def day_time_series(self, use):
        """
        以24小時去統計每一小時區間的使用次數
        不同站點，不同的統計圖
        計算完先儲存成 csv file

        例外發生描述:
        南港車站有不同的路口
        南港車站(興華路) 南港車站(忠孝東路)
        其他檔案也有類似情形
        """
        header = [(i, i + 1) for i in range(24)]
        for element in self.file_name:
            data = LoadData.load_refactor_ubike_timestamp(element)
            station_count = {}
            for station in self.station_type:
                station_count[station] = [0 for _ in range(24)]

            borrow_time, borrow_station = [], []
            if use == 'BorrowStation':
                borrow_time = [datetime.datetime.strptime(x, '%Y/%m/%d %H:%M:%S') for x in data['BorrowTime'].values]
                borrow_station = data['BorrowStation'].values
            elif use == 'ReturnStation':
                borrow_time = [datetime.datetime.strptime(x, '%Y/%m/%d %H:%M:%S') for x in data['ReturnTime'].values]
                borrow_station = data['ReturnStation'].values
            else:
                print('<---No this columns--->')

            for b_time, b_station in zip(borrow_time, borrow_station):
                try:
                    station_count[b_station][b_time.hour] += 1
                except KeyError as e:
                    for field in self.station_type:
                        if field.find(b_station) != -1:
                            station_count[field][b_time.hour] += 1

            day = borrow_time[0].date()
            pd_data = pd.DataFrame(station_count, index=header, columns=station_count.keys())
            Export.day_station_count(pd_data, day, use)

    @staticmethod
    def week_time_series(fname, ttype, utype):
        """
        以一周 7天去統計每一小時區間的使用次數
        開始天數往後推 7天, 第一天 2015-01-01 是禮拜四
        以 day_time_series 計算完的 csv 檔去產生新的 csv
        """
        header = ['Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed']
        idx = []
        pd_borrow_data, pd_return_data = (pd.DataFrame() for _ in range(2))
        for file, days in zip(fname, header):
            borrow_data, return_data = LoadData.load_station_count(file, ttype, utype)
            idx += [(days,) + make_tuple(x) for x in borrow_data.index]
            pd_borrow_data = pd.concat((pd_borrow_data, borrow_data), axis=0, ignore_index=True)
            pd_return_data = pd.concat((pd_return_data, return_data), axis=0, ignore_index=True)
        pd_borrow_data.index = idx
        pd_return_data.index = idx
        # print('pd_borrow_data\n', pd_borrow_data.head())
        # print('pd_return_data\n', pd_return_data.head())
        name = fname[0][6: 16] + '~' + fname[-1][6: 16]
        Export.week_station_count(pd_borrow_data, name, utype[0])
        Export.week_station_count(pd_return_data, name, utype[1])

    @staticmethod
    def month_time_series(fname, ttype, utype):
        """
        以一月的天數去統計每天的使用次數
        第一個月是 2015-01 ~ 2017-05
        以 day_time_series 計算完的 csv 檔去產生新的 csv
        """
        target_timestamp = np.array([])
        start_date = datetime.datetime(2015, 1, 1)
        end_date = datetime.datetime(2017, 5, 31)
        for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
            target_timestamp = np.append(target_timestamp, dt.strftime("%Y-%m"))
        # print('target_timestamp\n', target_timestamp)

        for timestamp in target_timestamp:
            element = [x for x in fname if x.find(timestamp) != -1]
            np_borrow, np_return = (np.array([]) for _ in range(2))
            idx = np.array([])
            columns = np.array([])

            for field in element:
                idx = np.append(idx, field[6: 16])
                borrow_data, return_data = LoadData.load_station_count(field, ttype, utype)
                if columns.size == 0:
                    columns = borrow_data.columns

                # np_data1-> sum of the borrow_data
                # np_data2-> sum of the return_data
                np_data1 = np.sum(borrow_data.values, axis=0).reshape(1, -1)
                np_data2 = np.sum(return_data.values, axis=0).reshape(1, -1)
                if np_borrow.size == 0:
                    np_borrow = np_data1
                else:
                    np_borrow = np.concatenate((np_borrow, np_data1), axis=0)

                if np_return.size == 0:
                    np_return = np_data2
                else:
                    np_return = np.concatenate((np_return, np_data2), axis=0)

            # print('np_borrow\n', np_borrow, np_borrow.shape)
            # print('np_return\n', np_return, np_return.shape)
            pd_borrow = pd.DataFrame(np_borrow, columns=columns, index=idx)
            pd_return = pd.DataFrame(np_return, columns=columns, index=idx)
            Export.month_station_count(pd_borrow, timestamp, utype[0])
            Export.month_station_count(pd_return, timestamp, utype[1])


# # Output the statistic data of the station as a csv file
used = ['BorrowStation', 'ReturnStation']
# used = ['ReturnStation']
#  bandwidths = ['Day', 'Week', 'Month']
print("<---0. Day--->")
print("<---1, Week--->")
print("<---2, Month--->")
bandwidths = input("<---Please choose and run program--->: ")

if int(bandwidths) == 0:
    file_name = LoadData.load_timestamp_fname()
    ts = TimeSeriesStatistic(file_name)
    for use in used:
        ts.day_time_series(use)

elif int(bandwidths) == 1:
    bandwidths = ['Day']
    used = ['BorrowStation', 'ReturnStation']
    file_name = LoadData.load_station_count_fname(bandwidths[0], used[0])
    print(file_name)
    for i in range(0, len(file_name), 7):
        TimeSeriesStatistic.week_time_series(file_name[i: i + 7], bandwidths[0], used)

elif int(bandwidths) == 2:
    bandwidths = ['Day']
    used = ['BorrowStation', 'ReturnStation']
    file_name = LoadData.load_station_count_fname(bandwidths[0], used[0])
    print(file_name)
    TimeSeriesStatistic.month_time_series(file_name, bandwidths[0], used)

else:
    print("You enter a wrong code")




