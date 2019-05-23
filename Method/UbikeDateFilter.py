"""
Data Clean(Ubike Charging Date)
"""

import pandas as pd

from Method.LoadData import LoadData

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)

file_name = LoadData.load_timestamp_fname()
# print('file_name', file_name)

station = LoadData.load_refactor_ubike_station()
sna = station['sna'].values
# print('station', station)

name = 'youbike_20150413.csv'
data = LoadData.load_ubike_timestamp(name)
new_data = data[data['BorrowStation'].isin(sna) & data['ReturnStation'].isin(sna)]
# print('new_data\n', new_data)
path = '../Data/NewUbike/Ubike/'+name
new_data.to_csv(path, index=False, encoding='utf_8_sig')

# for name in file_name:
#     data = LoadData.load_ubike_timestamp(name)
#     new_data = data[data['BorrowStation'].isin(sna) & data['ReturnStation'].isin(sna)]
#     # print('new_data\n', new_data)
#     path = '../Data/NewUbike/Ubike/'+name
#     new_data.to_csv(path, index=False, encoding='utf_8_sig')

# Test Data
# for name in file_name:
#     path = '../Data/NewUbike/Ubike/'+name
#     data = pd.read_csv(path)
#     print(data.head())