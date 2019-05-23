# -*- coding=utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from dateutil.rrule import rrule, DAILY, MONTHLY

from Method.LoadData import LoadData


def graph_by_day(borrow_file, return_file):
    """
    Month Graph(one Month)
    如果要畫一個月統計圖的話
    直接讀檔進行畫圖
    Ubike-DataMining\\Data\\NewUbike\\UbikeStatistic\\Month\\
    """

    sns.set(style='darkgrid')
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
    color_array = ['Blue', 'Red', 'Green']
    label_array = ['Borrow', 'Return', 'Total']

    for x, y in zip(borrow_file, return_file):

        # Open or Create a folder
        name = x[6: 13]
        path = "../Data/Graph/Statistic_Graph/Month/" + name
        if not os.path.isdir(path):
            os.mkdir(path)

        borrow_data = LoadData.load_month_borrow_data(x)
        return_data = LoadData.load_month_return_data(y)
        # print('borrow_data\n', borrow_data.head())
        # print('return_data\n', return_data.head())
        columns = borrow_data.columns
        idx = borrow_data.index
        x_data = np.array([i for i in range(len(idx))])

        for col in columns:
            fig, ax = plt.subplots(figsize=(16, 8), dpi=100)
            y1_data = borrow_data[col].values
            y2_data = return_data[col].values
            y3_data = y1_data + y2_data
            ax.plot(x_data, y1_data, color=color_array[0], label=label_array[0])
            ax.plot(x_data, y2_data, color=color_array[1], label=label_array[1])
            ax.plot(x_data, y3_data, color=color_array[2], label=label_array[2])

            plt.title(col+'('+name+')', fontproperties=myfont)
            plt.xlabel('時間軸', fontproperties=myfont)
            plt.ylabel('租借次數', fontproperties=myfont)
            plt.xticks(np.arange(len(idx)), idx, rotation=45, fontsize=12)
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
            # plt.ion()
            # plt.pause(1)
            plt.close()
            # plt.show()


def graph_by_hour(fname, ttype, utype):
    """
    Month Graph(Build One Month -> 24 hours on each day)
    Ubike-DataMining\\Data\\NewUbike\\UbikeStatistic\\Day\\
    """
    # Basic Setting
    header = [x[14: 16] for x in fname]
    sns.set(style='darkgrid')
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
    color_array = ['Blue', 'Red', 'Green']
    label_array = ['Borrow', 'Return', 'Total']
    line_size = 0.7

    # Open or Create a folder
    name = fname[0][6: 13]
    path = "../Data/Graph/Statistic_Graph/Month(hour)/" + name
    if not os.path.isdir(path):
        os.mkdir(path)

    # Load data and plot
    # x_data = np.array([i for i in range(24 * len(header))])
    pd_borrow_data, pd_return_data = (pd.DataFrame() for _ in range(2))
    for file in fname:
        borrow_data, return_data = LoadData.load_station_count(file, ttype, utype)
        pd_borrow_data = pd.concat((pd_borrow_data, borrow_data), axis=0)
        pd_return_data = pd.concat((pd_return_data, return_data), axis=0)

    for col in pd_borrow_data.columns:
        y1_data = pd_borrow_data[col].values
        y2_data = pd_return_data[col].values
        y3_data = y1_data + y2_data

        f, axarr = plt.subplots(3, 1, sharex='all', figsize=(16, 8), dpi=100)
        axarr[0].plot(y1_data, color=color_array[0], label=label_array[0], linewidth=line_size)
        axarr[1].plot(y2_data, color=color_array[1], label=label_array[1], linewidth=line_size)
        axarr[2].plot(y3_data, color=color_array[2], label=label_array[2], linewidth=line_size)

        # Graph Setting
        # plt.tight_layout()
        axarr[0].set_title(col+'(' + name + ')', fontproperties=myfont)
        plt.xticks(np.arange(0, 24*len(header), 24), header, rotation=0, fontsize=12)
        for sub_plot in axarr:
            sub_plot.legend(loc='upper right')
            sub_plot.set_ylim(ymin=0) if np.sum(y3_data) == 0 else sub_plot.set_ylim(ymin=0, ymax=np.max(y3_data))
            sub_plot.set_ylabel('次數', fontproperties=myfont)
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


print("<---0. Month (x-axis is one day)--->")
print("<---1. Month:Subplot (x-axis is one hour)--->")
instruction = input("<---Please choose and run program--->: ")

if int(instruction) == 0:
    # Generate the time series graph
    borrow_file_name = LoadData.load_month_borrow_fname()
    return_file_name = LoadData.load_month_return_fname()
    graph_by_day(borrow_file_name, return_file_name)

elif int(instruction) == 1:
    bandwidths = ['Day']
    used = ['BorrowStation', 'ReturnStation']
    file_name = LoadData.load_station_count_fname(bandwidths[0], used[0])
    # print(file_name)

    # 先產生該月的日期
    target_timestamp = np.array([])
    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2017, 5, 31)
    for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
        target_timestamp = np.append(target_timestamp, dt.strftime("%Y-%m"))

    # 統計屬於該月的資料集
    # print('target_timestamp', target_timestamp)
    for target in target_timestamp:
        target_day = []
        for file in file_name:
            if file.find(target) != -1:
                target_day.append(file)
        # print(target_day)
        graph_by_hour(target_day, bandwidths[0], used)

else:
    print('<---Error Instruction--->')