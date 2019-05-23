# -*- coding=utf-8 -*-

import os
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
import time

from Method.LoadData import LoadData


def generate_graph(fname, ttype, utype):
    """
    Make Daily Graph
    :param fname:
    :param ttype:
    :param utype:
    :return:
    """
    # Basic Setting
    sns.set(style='darkgrid')
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
    path = "../Data/Graph/Statistic_Graph/Day/" + fname[6: -2]
    if not os.path.isdir(path):
        os.mkdir(path)
    color_array = ['Blue', 'Red', 'Green']
    label_array = ['Borrow', 'Return', 'Total']

    # Load data and plot
    borrow_data, return_data = LoadData.load_station_count(fname, ttype, utype)

    # print('borrow_data\n', borrow_data.head())
    # print('return_data\n', return_data.head())
    # x=input()

    header = list(borrow_data.columns)
    x_data = np.array(borrow_data.index)
    print('x_data', x_data)

    x_data = np.array([i for i in range(24)])
    for col in header:
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
        y1_data = borrow_data[col].values.T
        y2_data = return_data[col].values.T
        y3_data = y1_data + y2_data
        ax.plot(x_data, y1_data, color=color_array[0], label=label_array[0])
        ax.plot(x_data, y2_data, color=color_array[1], label=label_array[1])
        ax.plot(x_data, y3_data, color=color_array[2], label=label_array[2])

        plt.title(col, fontproperties=myfont)
        plt.xlabel('Time')
        plt.ylabel('Count')
        plt.xticks(np.arange(24), borrow_data.index, rotation=45)
        if np.sum(y3_data) == 0:
            plt.ylim(ymin=0)
        else:
            plt.ylim(ymin=0, ymax=np.max(y3_data))

        # Put a nicer background color on the legend.
        legend = ax.legend(loc='upper right')
        legend.get_frame().set_facecolor('C0')
        try:
            photo_path = path + '/' + col + '.png'
            plt.savefig(photo_path)
        except FileNotFoundError:
            col = col.replace('/', '-')
            photo_path = path + '/' + col + '.png'
            plt.savefig(photo_path)
        plt.ion()
        plt.pause(1)
        plt.close()
        # plt.show()


# Generate the time series graph
bandwidths = ['Day']
used = ['BorrowStation', 'ReturnStation']
file_name = LoadData.load_station_count_fname(bandwidths[0], used[0])
print(file_name)
for i in range(0, 10, 1):
    generate_graph(file_name[i], bandwidths[0], used)
