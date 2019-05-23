import numpy as np
import pandas as pd
import datetime
from dateutil.rrule import rrule, DAILY, MONTHLY
import matplotlib.pyplot as plt
import json
from sklearn import metrics

from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster import cluster_visualizer

from LoadData import LoadData


borrow_file_name = LoadData.load_month_borrow_fname()
return_file_name = LoadData.load_month_return_fname()
target_timestamp = np.array([])
start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2016, 12, 31)
for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
    target_timestamp = np.append(target_timestamp, dt.strftime("%Y-%m"))

print('target_timestamp', target_timestamp)
x=input()

total_borrow_data = pd.DataFrame()
total_return_data = pd.DataFrame()
for count in range(int(len(target_timestamp) / 12)):
    title_name = ""
    total_borrow_data.drop(total_borrow_data.index, inplace=True)
    total_return_data.drop(total_return_data.index, inplace=True)

    for x, y in zip(borrow_file_name[12 * count: 12 * (count + 1)], return_file_name[12 * count: 12 * (count + 1)]):
        borrow_data = LoadData.load_month_borrow_data(x)
        return_data = LoadData.load_month_return_data(y)
        total_borrow_data = pd.concat((total_borrow_data, borrow_data), axis=0)
        total_return_data = pd.concat((total_return_data, return_data), axis=0)
    # print('borrow_data\n', total_borrow_data.shape)
    # print('return_data\n', total_return_data.shape)

    np_data = [np.array(total_borrow_data).T, np.array(total_return_data).T]
    # 進行 K-medoids 分群並視覺化
    # 執行兩次，一次borrow 一次return
    condition = ['Borrow', 'Return']
    for data_set, choose in zip(np_data, condition):

        k_number = [x for x in range(3, 11, 1)]
        evaluation_score = []
        cluster_record = {}
        for k in k_number:
            n_cluster = np.random.randint(low=0, high=len(data_set), size=k)
            kmedoids_instance = kmedoids(data_set, n_cluster)
            kmedoids_instance.process()
            clusters = kmedoids_instance.get_clusters()
            cluster_record[k] = clusters

            # 取得分群的質心
            # clusters = kmedoids_instance.get_medoids()

            # 將分群結果轉換為和每一列資料相對應的標籤
            clusters_label = [0 for i in range(len(data_set))]
            for i in range(len(clusters)):
                for j in clusters[i]:
                    clusters_label[j] = i
            evaluation_score.append(metrics.silhouette_score(data_set, clusters_label))

        # 根據不同分群去區分不同的週期變化
        # cluster_name = ['cluster ' + str(i) for i in range(k)]
        # cluster_data = {}
        # for key, value in zip(cluster_name, clusters):
        #     cluster_data[key] = value
        # path = '../Data/Cluster/'+target_timestamp[12*count][0:4]+'-'+choose+'.json'
        # with open(path, 'w', encoding='utf-8') as outfile:
        #     json.dump(cluster_data, outfile, indent=2)

        # 作圖來選擇 k 為多少是最好的選擇
        plt.plot(k_number, evaluation_score, label='silhouette_score('+choose+')')
        plt.legend()
        plt.ylim(-1, 1)
        plt.show()
