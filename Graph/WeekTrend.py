"""
# 資料集每168小時(1周)切一個區間
# 然後做趨勢圖的疊圖
# 要注意的是第一天要是星期一
# 像是2015-01-01是禮拜四，這樣要從2015-01-05的星期一開始
"""

import os
import numpy as np
import datetime
import matplotlib.pyplot as plt

from Method.LoadData import LoadData


def plot_trend(data, start, year):
    """
    做出趨勢的疊圖
    只拿第 5次反小波回去的波形來做疊圖
    全部的站點都要做
    :param data: 分解後的波形資料，
    :param start: 去檢查該年的第幾天開始
    :return:
    """
    delta = 24 * 7
    layer = ['_4', '_5']

    for key, value in data.items():
        # 先判斷是不是屬於第五反小波的 key 值
        if layer[0] in key[0] or layer[1] in key[0]:
            count = 0
            idx = start
            week_data = np.array([])
            while True:
                tmp = np.array(value[idx: idx + delta])
                if len(tmp) < delta:
                    break
                if week_data.size == 0:
                    week_data = tmp.reshape(-1, delta)
                else:
                    # axis = 0, 垂直, axis = 1, 水平
                    week_data = np.concatenate((week_data, tmp.reshape(-1, delta)), axis=0)
                count += 1
                idx += 168

            line_size = 0.8
            fig, ax = plt.subplots(1, figsize=(16, 8), dpi=80)
            random_color = np.random.rand(week_data.shape[1], 3)
            for element, color in zip(week_data, random_color):
                ax.plot(np.arange(len(element)), element,
                        c=color, linewidth=line_size, label='Len(Wavelet): ' + str(layer))

            # plt.legend(loc='upper right')
            ax.set_title(str(key))
            path = '../Data/Graph/WaveletTrend/' + str(year) + '/'
            if not os.path.exists(path):
                os.mkdir(path)
            photo = path + str(key) + '.png'
            plt.savefig(photo, dpi=100)
            # plt.show()
            plt.close()


years = [x for x in range(2015, 2017, 1)]
for year in years:
    wavelet_data = LoadData.load_wavelet_data(year)
    # print(len(wavelet_data.keys()))
    # print(len(wavelet_data.values()))

    # 檢查一年的第一天維星期幾
    today_week = datetime.datetime.strptime(str(year)+'-'+'01'+'-'+'01', '%Y-%m-%d').weekday()
    # start_day = datetime.datetime.strptime(str(year)+'-'+'01'+'-'+'01', '%Y-%m-%d') + \
    #             datetime.timedelta(days=(7 - today_week))
    # print(start_day)

    plot_trend(wavelet_data, 7 - today_week, year)
