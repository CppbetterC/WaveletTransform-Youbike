"""
這份程式碼做的動作是將時間序列的資料進行小波分解
目的是要去看 x軸的資料集在分解幾次後可以看出長期的趨勢
x-axis, 時間序列的時間軸，最小單位是小時，讀檔的資料集是一整年 (24hr * 365days)
y-axis, 租借的次數
租借的類型有borrow和return兩種
"""

import numpy as np
import pandas as pd
import pywt
import datetime
import time
from dateutil.rrule import rrule, DAILY, MONTHLY

from Method.LoadData import LoadData
from Method.WaveletTransform import WaveletTransform


def generate_target_timeseries(start_year, end_year):
    """
    先產生一年的日期間，以每天為間隔
    儲存的資料結構為 dict
    key: (year, year+1)
    values: np.array([資料集])
    :return:
    """
    target_timestamp = {}
    iterval = [x for x in range(start_year, end_year, 1)]
    for year in iterval:
        start_date = datetime.datetime(year, 1, 1)
        end_date = datetime.datetime(year, 12, 31)
        tmp = np.array([])
        for dt in rrule(DAILY, dtstart=start_date, until=end_date):
            tmp = np.append(tmp, 'count(' + dt.strftime("%Y-%m-%d")+').csv')
        target_timestamp[(str(year), str(year+1))] = tmp
    return target_timestamp


start = time.time()

# 小波分解的層數
layer = 15

# 起始年和到哪年為止
syear = 2015
eyear = 2016
timeseries = generate_target_timeseries(syear, eyear)


# 讀檔，將每個csv檔案的資料取出
for series, target_timestamp in timeseries.items():
    total_borrow_data = pd.DataFrame()
    total_return_data = pd.DataFrame()
    for target in target_timestamp:
        borrow_data, return_data = LoadData.load_station_count(target, 'Day', ['BorrowStation', 'ReturnStation'])
        total_borrow_data = pd.concat((total_borrow_data, borrow_data), axis=0)
        total_return_data = pd.concat((total_return_data, return_data), axis=0)
    #
    print(total_borrow_data.shape)
    print(total_return_data.shape)

    # 進行小波分解(0 ~ N 層)
    # 並做出相對應的小波分解後的視覺化圖
    algorithm = pywt.Wavelet('db2')
    wavelet = WaveletTransform(
        total_borrow_data, total_return_data, int(layer), algorithm, interval=series[0])
    wavelet.fit_transform()

end = time.time()
print('Cost Time', end-start)
