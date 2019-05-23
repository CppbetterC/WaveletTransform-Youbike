import os
import json
import demjson
import pandas as pd
from ast import literal_eval as make_tuple


class LoadData:

    @staticmethod
    def load_ubike_station():
        """
        Load the data of the ubkie station.csv
        :return:
        """
        rel_path = '../Data/YouBike/youbikeStation.csv'
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data = pd.read_csv(abs_path, encoding='utf-8')
        return data

    @staticmethod
    def load_ubike_timestamp(name):
        """
        Load the ubike date .csv
        :param name:
        :return:
        """
        rel_path = '../Data/YouBike/YOUBIKEDATE/'+str(name)
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data = pd.read_csv(abs_path, encoding='utf-8')
        return data

    @staticmethod
    def load_timestamp_fname():
        """
        Load the all file name in this path
        :return: file name
        """
        rel_path = '../Data/YouBike/YOUBIKEDATE/'
        file_name = []
        with os.scandir(rel_path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    file_name.append(entry.name)
        return file_name

    @staticmethod
    def load_refactor_ubike_station():
        """
        Load the data of the refactor ubkie station.csv(雙北地區)
        :return:
        """
        rel_path = '../Data/NewUbike/youbikeStation.csv'
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data = pd.read_csv(abs_path, encoding='utf-8')
        return data

    @staticmethod
    def load_refactor_ubike_timestamp(name):
        """
        Load the ubike date .csv
        :param name:
        :return:
        """
        rel_path = '../Data/NewUbike/Ubike/'+str(name)
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data = pd.read_csv(abs_path, encoding='utf-8')
        return data

    @staticmethod
    def load_station_count_fname(ttype, utype):
        """
        Load the all file name in this path
        :return: file name
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/'+str(ttype)+'/'+str(utype)
        file_name = []
        with os.scandir(rel_path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    file_name.append(entry.name)
        return file_name

    @staticmethod
    def load_station_count(name, ttype, utype):
        """
        Load the station_count(xxxx-xx-xx).csv
        :param name:
        :param ttype: 時間的差別(day, week, month)
        :param utype: 使用的差別(borrow, return)
        :return:
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/'+str(ttype)+'/'+str(utype[0])+'/'+str(name)
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data1 = pd.read_csv(abs_path, encoding='utf-8', index_col=0)

        rel_path = '../Data/NewUbike/UbikeStatistic/'+str(ttype)+'/'+str(utype[1])+'/'+str(name)
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data2 = pd.read_csv(abs_path, encoding='utf-8', index_col=0)
        return data1, data2

    @staticmethod
    def load_month_borrow_fname():
        """
        讀出所有屬於該月的資料
        :return:
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/Month/BorrowStation'
        file_name = []
        with os.scandir(rel_path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    file_name.append(entry.name)
        return file_name

    @staticmethod
    def load_month_borrow_data(file):
        rel_path = '../Data/NewUbike/UbikeStatistic/Month/BorrowStation/'+str(file)
        data = pd.read_csv(rel_path, encoding='utf-8', index_col=0)
        return data

    @staticmethod
    def load_month_return_fname():
        """
        讀出所有屬於該月的資料
        :return:
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/Month/ReturnStation'
        file_name = []
        with os.scandir(rel_path) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    file_name.append(entry.name)
        return file_name

    @staticmethod
    def load_month_return_data(file):
        rel_path = '../Data/NewUbike/UbikeStatistic/Month/ReturnStation/'+str(file)
        data = pd.read_csv(rel_path, encoding='utf-8', index_col=0)
        return data

    @staticmethod
    def load_wavelet_data(year):
        rel_path = '../Data/' + str(year) + 'Inverse_Wavelet_data.txt'
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data = {}
        with open(abs_path, 'r', encoding='utf-8') as file_handle:
            for line in file_handle.readlines():
                field = line.split('|')
                data[make_tuple(field[0])] = make_tuple(field[1])
        return data
