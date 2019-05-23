"""
實作統計租借站的借用量，用於自定義每個站點屬於哪類的租借站點
並先刪除時間序列資料中有某一週的租借量皆為0的情況
找出較能夠代表不同分類的租借站點，最後挑出租用量最高的3高代表該群站點。
先粗略分三類，(鄰近上班地點、鄰近觀光景點、鄰近住宅區)
"""

import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from Method.LoadData import LoadData


def cluster(data, start, end, year):
    """
    :param data: 分解後的波形資料，
    :param start: 去檢查該年的第幾天開始
    :param end:  去檢查該年的最後一天到什麼時候
    :param year: 第幾年的資料
    :return:
    """

    # np_data = value[start: end]
    # 做分群圖(KMeans)
    values = np.array(list(data.values()))
    scaler = MinMaxScaler(feature_range=(-1, 1))
    norm_data = scaler.fit_transform(values[:, start: end])

    dim = 3
    pca = PCA(n_components=dim)
    new_data = pca.fit_transform(norm_data)

    cluster = 5
    kmeans = KMeans(n_clusters=cluster).fit(new_data)
    cluster_label = kmeans.labels_

    fig = plt.figure(figsize=(16, 8), dpi=100)
    ax = Axes3D(fig)

    ax.scatter(new_data[:, 0], new_data[:, 1], new_data[:, 2], c=cluster_label)
    ax.set_title('Station Cluster')
    # count = 1
    # for x in new_data:
    #     ax.text(x[0], x[1], x[2], '%s' % (str(count)), size=10, zorder=1, color='grey')
    #     count += 1

    path = '../Data/Graph/Clustering/'
    if not os.path.exists(path):
        os.mkdir(path)
    photo = path + str(key) + '.png'
    # plt.savefig(photo, dpi=100)
    plt.show()
    # plt.close()




for year in [x for x in range(2015, 2016, 1)]:
    wavelet_data = LoadData.load_wavelet_data(year)
    first_week = datetime.datetime.strptime(str(year) + '-' + '01' + '-' + '01', '%Y-%m-%d').weekday()
    last_week = datetime.datetime.strptime(str(year) + '-' + '12' + '-' + '31', '%Y-%m-%d').weekday()

    array = list(wavelet_data.keys())
    limit_array = {}
    cnt = 0
    for key, value in wavelet_data.items():
        if '_3' in key[0]:
            limit_array[(cnt, key[0])] = value
    # print(limit_array)

    cluster(limit_array, 7 - first_week, -1 - last_week, year)
    # print('Station\n', station)
    # print('len(Station)', len(station))
