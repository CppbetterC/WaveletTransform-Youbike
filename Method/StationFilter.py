"""
Data Clean(Ubike Station)
"""

import pandas as pd

from Method.LoadData import LoadData


def ubkike_station_clean(data):
    taipei_area = ['中正區', '大同區', '中山區', '松山區', '大安區',
                   '萬華區', '信義區', '士林區', '北投區', '內湖區',
                   '南港區', '文山區']

    new_taipei_area = ['板橋區', '中和區', '新莊區', '土城區', '汐止區',
                       '鶯歌區', '淡水區', '五股區', '林口區', '深坑區',
                       '坪林區', '石門區', '萬里區', '雙溪區', '烏來區',
                       '三重區', '永和區', '新店區', '蘆洲區', '樹林區',
                       '三峽區', '瑞芳區', '泰山區', '八里區', '石碇區',
                       '三芝區', '金山區', '平溪區', '貢寮區']
    collection = set(taipei_area + new_taipei_area)
    new_data = data[data['sarea'].isin(collection)]
    return new_data


ubike_station = LoadData.load_ubike_station()
# print('ubike_station\n', ubike_station.head())

new_ubike_station = ubkike_station_clean(ubike_station)
path = '../Data/NewUbike/youbikeStation.csv'
new_ubike_station.to_csv(path, index=False, encoding='utf_8_sig')

data = pd.read_csv(path)
print(data.head())
