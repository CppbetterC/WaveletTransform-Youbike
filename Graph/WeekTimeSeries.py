# -*- coding=utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as datetime
from ast import literal_eval as make_tuple

from Method.LoadData import LoadData


def generate_graph(fname, ttype, utype):
    """
    Week Graph(Monday~Sunday)
    如果要畫一周圖的話，可以每次都先讀入 7份csv檔案來作圖
    :param fname: file name
    :param ttype: Week
    :param utype: Borrow, Return
    :return:
    """
    # Basic Setting
    header = ['Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed']
    sns.set(style='darkgrid')
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
    path = "../Data/Graph/Statistic_Graph/Week/" + fname[0][6: 16] + '~' + fname[-1][6: 16]
    if not os.path.isdir(path):
        os.mkdir(path)
    color_array = ['Blue', 'Red', 'Green']
    label_array = ['Borrow', 'Return', 'Total']

    # Load data and plot
    x_data = np.array([i for i in range(24 * len(header))])
    pd_borrow_data, pd_return_data = (pd.DataFrame() for _ in range(2))
    for file in fname:
        borrow_data, return_data = LoadData.load_station_count(file, ttype, utype)
        pd_borrow_data = pd.concat((pd_borrow_data, borrow_data), axis=0)
        pd_return_data = pd.concat((pd_return_data, return_data), axis=0)

    for col in pd_borrow_data.columns:
        fig, ax = plt.subplots(figsize=(16, 8), dpi=100)
        y1_data = pd_borrow_data[col].values
        y2_data = pd_return_data[col].values
        y3_data = y1_data + y2_data
        ax.plot(x_data, y1_data, color=color_array[0], label=label_array[0])
        ax.plot(x_data, y2_data, color=color_array[1], label=label_array[1])
        ax.plot(x_data, y3_data, color=color_array[2], label=label_array[2])

        plt.title(col+'('+fname[0][6: 16]+'~'+fname[-1][6: 16]+')', fontproperties=myfont)
        plt.xlabel('時間軸', fontproperties=myfont)
        plt.ylabel('租借次數', fontproperties=myfont)
        plt.xticks(np.arange(0, 24*len(header), 24), header, rotation=45, fontsize=12)
        # plt.xticks(range(len(header)), rotation=45)
        if np.sum(y3_data) == 0:
            plt.ylim(ymin=0)
        else:
            plt.ylim(ymin=0, ymax=np.max(y3_data))

        # Put a nicer background color on the legend.
        legend = ax.legend(loc='upper right')
        legend.get_frame().set_facecolor('C0')
        # manager = plt.get_current_fig_manager()
        # manager.window.showMaximized()
        try:
            photo_path = path + '/' + col + '.png'
            plt.savefig(photo_path)
        except FileNotFoundError:
            col = col.replace('/', '-')
            photo_path = path + '/' + col + '.png'
            plt.savefig(photo_path)
        # plt.ion()
        # plt.pause(1)
        plt.close()
        # plt.show()


# Generate the time series graph
bandwidths = ['Day']
used = ['BorrowStation', 'ReturnStation']
file_name = LoadData.load_station_count_fname(bandwidths[0], used[0])
print(file_name)
for i in range(0, len(file_name), 7):
    generate_graph(file_name[i: i+7], bandwidths[0], used)
