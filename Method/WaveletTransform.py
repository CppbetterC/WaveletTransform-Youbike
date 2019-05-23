"""
小波轉換（Wavelet Transform）
"""

import os
import json
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

import pywt


class WaveletTransform:

    def __init__(self, borrow_data, return_data, layer, algorithm, interval=None):
        """
        :param borrow_data:
        :param return_data:
        :param layer: 要分解幾層
        :param algorithm: 要使用哪種小波家族的波形去分解
        :param interval: 屬於哪年的資料
        """
        # print('<---Show the wavelet family--->')
        # for family in pywt.families():
        #     print("%s family: " % family + ', '.join(pywt.wavelist(family)))
        self.__layer = layer
        self.__algorithm = algorithm
        self.__column = borrow_data.columns
        self.__borrow_data = borrow_data
        self.__return_data = return_data
        self.__interval = interval

    def fit_transform(self):
        # 每個租借站點都要小波分解
        for element in self.__column:
            borrow_data = self.__borrow_data[element].values
            return_data = self.__return_data[element].values

            if np.sum(borrow_data) == 0 or np.sum(return_data) == 0:
                continue

            # 做兩次、一次借一次還
            # coef_mas 紀錄高頻波和低頻波的資料集
            # result 紀錄分解出來的高頻波和低頻波還原回去的波形資料集
            result = {}
            choose = ['Borrow', 'Return']
            for i in range(len(choose)):
                data = borrow_data if choose[i] == 'Borrow' else return_data
                for index in range(1, self.__layer+1, 1):
                    # 分解 && 做小波分解迭代圖
                    cA, cD = pywt.dwt(data, self.__algorithm)  # Approximation and detail coefficients.
                    result[(choose[i], index)] = [cA, cD]
                    data = cA

                    # 分解成高頻和低頻的波
                    self.plot(cA, cD, choose[i], itr=str(index), station=element)

            # 做小波分解擬合圖
            self.plot_fitting_graph(wave_data=result, station=element)

            # 每一周(168小時)切一段來做合須圖和疊圖，先儲存此段資料
            # self.inverse_wavelet_data(wave_data=result, station=element)

            # 只輸出最後一次的小波分解時間序列資料，用斜率看一年的趨勢
            # self.save_final_wavelet_data(result, element)

    def plot(self, cA, cD, category, itr=None, station=None):
        """
        :param cA: 高頻波
        :param cD: 低頻波
        :param idx: 租借或歸還行為
        :param itr: 第幾次分解
        :param station: 租借站點名稱
        :return:
        """
        f, axarr = plt.subplots(2, sharex='all', figsize=(18, 9))
        axarr[0].plot(cA, c='black', label='low-frequency')
        if itr:
            axarr[0].set_title(station + '-' + category + '-(Iteration ' + str(itr) + ')')

        axarr[1].plot(cD, c="grey", label='high-frequency')
        axarr[0].legend(loc='upper right')
        axarr[1].legend(loc='upper right')

        # path = '..\\Data\\Graph\\WaveletTransform\\Month(hour)\\' + self.__interval + '\\'
        path = '..\\Data\\Graph\\WaveletTransform\\Year\\' + self.__interval + '\\'
        if not os.path.exists(path):
            os.mkdir(path)

        try:
            photo = path + station + '\\' + category + '(Iteration ' + str(itr) + ')' + '.png'
            plt.savefig(photo, dpi=100)
        except FileNotFoundError:
            if station.find('/') != -1:
                station = station.replace('/', '-')
                if not os.path.exists(path + station):
                    os.mkdir(path + station + '\\')
                photo = path + station + '\\' + category + '(Iteration ' + str(itr) + ')' + '.png'
                plt.savefig(photo, dpi=100)
            else:
                os.mkdir(path + station + '\\')
                photo = path + station + '\\' + category + '(Iteration ' + str(itr) + ')' + '.png'
                plt.savefig(photo, dpi=100)
        # plt.show()
        plt.close()

    def plot_fitting_graph(self, wave_data, station):
        """
        作出第 i次小波分解和第原始的波形
        去擬合看看周期、規律
        :param wave_data: 已分解出的小波波形資料
        :param station: 租借站點名
        :return:
        """

        for key, value in wave_data.items():
            # 還原到最原始的波型
            # key為一個tuple, ('Borrow', 4) or ('Return', 3)
            inverse_high_wave = self.inverse_dwt(key, value)
            if key[0] == 'Borrow':
                org_high_wave = self.__borrow_data[station].values
            else:
                org_high_wave = self.__return_data[station].values

            fig, ax = plt.subplots(1, figsize=(16, 8), dpi=80)
            ax.plot(np.arange(len(org_high_wave)), org_high_wave, color='grey', label='Original Wave')
            ax.plot(
                np.arange(len(inverse_high_wave)), inverse_high_wave, color='black',
                label='low-frequent iteration '+str(key[1])
            )
            plt.legend(loc='upper right')
            ax.set_title(station + '-' + str(key))

            station_token = station
            if station.find('/') != -1:
                station_token = station.replace('/', '-')
            path = '..\\Data\\Graph\\WaveletTransform\\Year\\' + self.__interval + '\\' + station_token + '\\'
            if not os.path.exists(path):
                os.mkdir(path)
            photo = path + key[0] + 'Original and iteration' + str(key[1]) + '.png'
            plt.savefig(photo, dpi=100)
            # plt.show()
            plt.close()

    def inverse_dwt(self, itr, data):
        """
        幫助已經小波分解的波
        重構回去最原始的波形
        :param itr: 波要返回去的次數
        :param data:
        :return:
        """
        low_wave = data[0]
        for i in range(itr[1]):
            tmp_high_wave = pywt.idwt(low_wave, None, self.__algorithm, 'symmetric')
            low_wave = tmp_high_wave
        return low_wave

    def inverse_wavelet_data(self, wave_data, station):
        """
        作出第 i次小波分解的反小波波形資料並將之儲存為 DataFrame
        :param wave_data: 已分解出的小波波形資料
        :param station: 租借站點名
        :return:
        """
        limit = 24 * 366
        data = {}
        for key, value in wave_data.items():
            # 還原到最原始的波型
            # key為一個tuple, ('Borrow', 4) or ('Return', 3)
            inverse_low_wave = self.inverse_dwt(key, value)
            if len(inverse_low_wave) > limit:
                continue
            data[station+'_'+str(key[0])+'_'+str(key[1])] = inverse_low_wave.tolist()

        path = '../Data/' + self.__interval + 'Inverse_Wavelet_data.txt'
        with open(path, 'a+', encoding='utf-8') as f:
            for key, value in data.items():
                f.writelines(str(tuple([key]))+'|'+str(tuple(value)))
                f.writelines('\n')

    def save_final_wavelet_data(self, wave_data, station):
        borrow_data = wave_data[('Borrow', self.__layer)][0]
        path = '../Data/' + self.__interval + 'Final_Wavelet_Trend(Borrow).txt'
        with open(path, 'a+', encoding='utf-8') as f:
            f.writelines(str(tuple([station]))+'|'+str(tuple(borrow_data)))
            f.writelines('\n')

        return_data = wave_data[('Return', self.__layer)][0]
        path = '../Data/' + self.__interval + 'Final_Wavelet_Trend(Return).txt'
        with open(path, 'a+', encoding='utf-8') as f:
            f.writelines(str(tuple([station]))+'|'+str(tuple(return_data)))
            f.writelines('\n')