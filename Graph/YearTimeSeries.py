# -*- coding=utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import seaborn as sns
import datetime
from dateutil.rrule import rrule, DAILY, MONTHLY, YEARLY

from Method.LoadData import LoadData


def build_timestamp():
    """
    先產生屬於該年的的月份
    :return:
    """
    target_timestamp = np.array([])
    start_date = datetime.datetime(2015, 1, 1)
    end_date = datetime.datetime(2016, 12, 31)
    for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
        target_timestamp = np.append(target_timestamp, dt.strftime("%Y-%m"))
    # print('target_timestamp', target_timestamp)
    return target_timestamp


def graph_by_day(borrow_file, return_file, condition):
    """
    Year Graph(x-axis is one day)
    如果要畫一年統計圖的話
    先取得一年各月的資訊再讀檔進行畫圖
    Ubike-DataMining\\Data\\NewUbike\\UbikeStatistic\\Month\\
    condition 代表是否要做組圖
    """

    sns.set(style='darkgrid')
    myfont = fm.FontProperties(fname='C:/Windows/Fonts/msyh.ttc')
    color_array = ['Blue', 'Red', 'Green']
    label_array = ['Borrow', 'Return', 'Total']

    timestamp = build_timestamp()
    # print('target_timestamp', timestamp)
    for count in range(int(len(timestamp) / 12)):
        title_name = ""
        total_borrow_data = pd.DataFrame()
        total_return_data = pd.DataFrame()
        for x, y in zip(borrow_file[12*count: 12*(count+1)], return_file[12*count: 12*(count+1)]):
            # Open or Create a folder
            title_name = x[6: 10]
            if condition == 1:
                path = "../Data/Graph/Statistic_Graph/Year/" + title_name
            else:
                path = "../Data/Graph/Statistic_Graph/Year(Subplots)/" + title_name

            if not os.path.isdir(path):
                os.mkdir(path)

            borrow_data = LoadData.load_month_borrow_data(x)
            return_data = LoadData.load_month_return_data(y)
            # print('borrow_data\n', borrow_data.head())
            # print('return_data\n', return_data.head())

            total_borrow_data = pd.concat((total_borrow_data, borrow_data), axis=0)
            total_return_data = pd.concat((total_return_data, return_data), axis=0)
        # print('borrow_data\n', total_borrow_data.shape)
        # print('return_data\n', total_return_data.shape)

        columns = total_borrow_data.columns
        # idx = total_borrow_data.index
        x_data = np.array([i for i in range(len(total_borrow_data.index))])
        # xticks = timestamp[12*count: 12*(count+1)]

        for col in columns:
            if condition == 1:
                fig, ax = plt.subplots(figsize=(16, 8), dpi=100)
                y1_data = total_borrow_data[col].values
                y2_data = total_return_data[col].values
                # y3_data = y1_data + y2_data
                ax.plot(x_data, y1_data, color=color_array[0], label=label_array[0])
                ax.plot(x_data, y2_data, color=color_array[1], label=label_array[1])
                # ax.plot(x_data, y3_data, color=color_array[2], label=label_array[2])

                # year = mdates.YearLocator()
                # month = mdates.MonthLocator()
                # day = mdates.DayLocator()
                # date_format = mdates.DateFormatter("%Y-%m")
                # ax.xaxis.set_major_locator(year)
                # ax.xaxis.set_major_locator(month)
                # ax.xaxis.set_major_locator(day)
                # ax.xaxis.set_major_formatter(date_format)
                # fig.autofmt_xdate()

                plt.title(col+'('+title_name+')', fontproperties=myfont)
                plt.xlabel('時間軸', fontproperties=myfont)
                plt.ylabel('租借次數', fontproperties=myfont)
                # print('xticks', xticks)
                # plt.xticks(np.arange(len(xticks)), xticks, rotation=45, fontsize=12)

                # plt.margins(x=0, y=0)

                # if np.sum(y3_data) == 0:
                #     plt.ylim(ymin=0)
                # else:
                #     plt.ylim(ymin=0, ymax=np.max(y3_data))

                # Put a nicer background color on the legend.
                legend = ax.legend(loc='upper right')
                legend.get_frame().set_facecolor('C0')

                path = "../Data/Graph/Statistic_Graph/Year/" + title_name
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
            # 組合圖
            else:
                fig, ax = plt.subplots(2, sharex='all', figsize=(16, 8), dpi=100)
                y1_data = total_borrow_data[col].values
                y2_data = total_return_data[col].values
                ax[0].plot(x_data, y1_data, color=color_array[0], label=label_array[0])
                ax[1].plot(x_data, y2_data, color=color_array[1], label=label_array[1])

                ax[0].set_title(col+'('+title_name+')', fontproperties=myfont)
                ax[1].set_xlabel('時間軸', fontproperties=myfont)
                ax[1].set_ylabel('租借次數', fontproperties=myfont)

                ax[0].legend(loc='upper right')
                ax[1].legend(loc='upper right')

                path = "../Data/Graph/Statistic_Graph/Year(Subplots)/" + title_name
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
borrow_file_name = LoadData.load_month_borrow_fname()
return_file_name = LoadData.load_month_return_fname()

print('<---1. 同一張圖--->')
print('<---2. 組合圖--->')
choose = input('<---Please input the condition--->: ')

if int(choose) == 1 or int(choose) == 2:
    graph_by_day(borrow_file_name, return_file_name, int(choose))
else:
    print('<---Error Condition--->')
