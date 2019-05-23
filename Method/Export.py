import os
import json
import pandas as pd


class Export:

    @staticmethod
    def day_station_count(data, date, used_type):
        """
        Export the station count as json file
        Statistic from the youbike_20150101.csv
        :param data: statistic data
        :param date:
        :return:
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/Day/'+str(used_type)+'/count('+str(date)+').csv'
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data.to_csv(abs_path, encoding='utf_8_sig')

    @staticmethod
    def week_station_count(data, series, used_type):
        """
        Export the station count as json file (Week Statistic)
        :param data: statistic data
        :param date:
        :return:
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/Week/'+str(used_type)+'/count('+str(series)+').csv'
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data.to_csv(abs_path, encoding='utf_8_sig')

    @staticmethod
    def month_station_count(data, series, used_type):
        """
        Export the station count as json file (Month Statistic)
        :param data: statistic data
        :param date:
        :return:
        """
        rel_path = '../Data/NewUbike/UbikeStatistic/Month/'+str(used_type)+'/count('+str(series)+').csv'
        abs_path = os.path.join(os.path.dirname(__file__), rel_path)
        data.to_csv(abs_path, encoding='utf_8_sig')
