"""
將每個站點的時間序列資料(波形資料)進行分群，
藉此分析該個租借站點那幾週的波形資料是較相近的，
可以說明一年52週，有哪幾週會是相似的類型。
"""

import os
import numpy as np
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from Method.LoadData import LoadData


def wavelet_clustering(data, start, year):
    """
    做出52週波形趨勢的分群
    拿第三次小波分解反小波的波形資料
    :param data: 分解後的波形資料，
    :param start: 去檢查該年的第幾天開始
    :param year: 第幾年的資料
    :return:
    """
    delta = 24 * 7
    layer = ['_3']

    for key, value in data.items():
        if layer[0] in key[0]:
            idx = start
            week_data = np.array([])
            while True:
                tmp = np.array(value[idx: idx + delta])
                # 防止最後一周的資料不滿 delta 個
                if len(tmp) < delta:
                    break
                if week_data.size == 0:
                    week_data = tmp.reshape(-1, delta)
                else:
                    # axis = 0, 垂直, axis = 1, 水平
                    week_data = np.concatenate((week_data, tmp.reshape(-1, delta)), axis=0)
                idx += 168

            # 做分群圖(KMeans)
            scaler = MinMaxScaler(feature_range=(-1, 1))
            norm_data = scaler.fit_transform(week_data)

            cluster = 3
            kmeans = KMeans(n_clusters=cluster).fit(norm_data)
            cluster_label = kmeans.labels_

            dim = 2
            pca = PCA(n_components=dim)
            new_data = pca.fit_transform(norm_data)

            # fig, ax = plt.figure(figsize=(16, 8), dpi=100)
            # ax = Axes3D(fig)
            fig, ax = plt.subplots(1, figsize=(16, 8), dpi=100)

            # ax.scatter(new_data[:, 0], new_data[:, 1], new_data[:, 2], c=cluster_label)
            ax.scatter(new_data[:, 0], new_data[:, 1], c=cluster_label)
            ax.set_title(str(key))
            count = 1
            for x in new_data:
                ax.text(x[0], x[1], '%s' % (str(count)), size=11, zorder=1, color='grey')
                count += 1

            if '/' in str(key):
                key = str(key).replace('/', '-')

            path = '../Data/Graph/Clustering/' + str(year) + '/'
            if not os.path.exists(path):
                os.mkdir(path)
            photo = path + str(key) + '.png'
            plt.savefig(photo, dpi=100)
            # plt.show()
            plt.close()


years = [x for x in range(2015, 2016, 1)]
for year in years:
    wavelet_data = LoadData.load_wavelet_data(year)
    # print(wavelet_data.keys())
    # print(len(wavelet_data.values()))

    # 檢查一年的第一天維星期幾
    # 目的在於一週的第一天是從星期一開始
    today_week = datetime.datetime.strptime(str(year)+'-'+'01'+'-'+'01', '%Y-%m-%d').weekday()
    wavelet_clustering(wavelet_data, 7 - today_week, year)