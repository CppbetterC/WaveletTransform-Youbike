"""
# 資料集每168小時(1周)切一個區間
# 然後做趨勢圖的疊圖
# 要注意的是第一天要是星期一
# 像是2015-01-01是禮拜四，這樣要從2015-01-05的星期一開始
"""

import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns

from Method.LoadData import LoadData


def box_plot(data, start, year):
    """
    拿第 5次反小波回去的波形資料來做合須圖
    每 7天做一張合須圖，一張合須圖包含所有佔點的資訊
    """
    delta = 24 * 7
    idx = start
    header = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    while True:
        np_data = np.array([])
        week_data = np.array(data[:, idx:idx+delta])
        for i in range(7):
            slice_tmp = week_data[:, i*24:(i+1)*24]
            sum_tmp = np.sum(slice_tmp, axis=1)
            # print(sum_tmp.shape)
            if np_data.size == 0:
                np_data = sum_tmp.reshape(sum_tmp.shape[0], -1)
                # print(np_data.shape)
            else:
                np_data = np.concatenate((np_data, sum_tmp.reshape(sum_tmp.shape[0], -1)), axis=1)
                # print(np_data.shape)

        pd_data = pd.DataFrame(np_data, columns=header)
        idx += 168

        print(len(pd_data))
        print(pd_data.head())
        myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
        sns.set(style="whitegrid")
        ax = sns.boxplot(data=pd_data)
        ax = sns.swarmplot(data=pd_data, color='.25')
        # random_color = np.random.rand(week_data.shape[1], 3)
        plt.title(str(key)+'-BoxPlot', fontproperties=myfont)
        plt.xticks([y + 1 for y in range(7)], header)

        # path = '../Data/Graph/WaveletTrend/' + str(year) + '/'
        # if not os.path.exists(path):
        #     os.mkdir(path)
        # photo = path + str(key) + '-BoxPlot-' + '.png'
        # plt.savefig(photo, dpi=100)
        plt.show()
        # plt.close()


years = [x for x in range(2015, 2017, 1)]
for year in years:
    wavelet_data = LoadData.load_wavelet_data(year)

    # key = wavelet_data.keys()
    # value = wavelet_data.values()
    # print(len(key))
    # print(len(value))
    layer = ['_4', '_5']
    idx, data_layer4, data_layer5 = (np.array([]) for _ in range(3))
    limit = 24 * 365
    for key, value in wavelet_data.items():
        if layer[0] in key[0]:
            idx = np.append(idx, np.array([key[0]]))
            data_layer4 = np.append(data_layer4, np.array(value[:limit]))
        if layer[1] in key[0]:
            data_layer5 = np.append(data_layer5, np.array(value[:limit]))

    data_layer4 = data_layer4.reshape(len(idx), -1)
    data_layer5 = data_layer5.reshape(len(idx), -1)

    print(data_layer4.shape)
    print(data_layer5.shape)

    # 檢查一年的第一天維星期幾
    today_week = datetime.datetime.strptime(str(year)+'-'+'01'+'-'+'01', '%Y-%m-%d').weekday()
    box_plot(data_layer4, 7 - today_week, year)
    box_plot(data_layer5, 7 - today_week, year)



