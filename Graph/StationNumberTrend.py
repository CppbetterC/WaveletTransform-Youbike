"""
實作Ubike站點的Bubble Chart
"""

import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
from ast import literal_eval as make_tuple

from sklearn.preprocessing import MinMaxScaler

from Method.LoadData import LoadData

# plotly.tools.set_credentials_file(username='-Ren-', api_key='DNnX5s0iZwH24b2qb4Zo')

mapbox_access_token = pd.read_json('../Data/PlotlyToken.json', typ='series')
print(mapbox_access_token['token'])

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)

# Load ubike station
# ubike_station = LoadData.load_ubike_station()
ubike_station = LoadData.load_refactor_ubike_station()
# print('ubike_station\n', ubike_station.head())

ubike_slice = ubike_station.loc[:, ['sna', 'lat', 'lng']]
# print(ubike_slice.head())

header = ['sna', 'attr1', 'attr2', 'attr3', 'slope', 'color']
borrow_data = pd.DataFrame(columns=header)
return_data = pd.DataFrame(columns=header)
year = 2015
path = '../Data/'+str(year)+'Final_Wavelet_Trend(Borrow).txt'
with open(path, 'r', encoding='utf-8') as file_handle:
    for line in file_handle.readlines():
        field = line.split('|')
        sname = list(make_tuple(field[0]))
        wdata = list(make_tuple(field[1]))
        slope = [(wdata[0] - wdata[-1]) / (0 - len(wdata))]
        pcolor = ['blue' if slope[0] > 0 else 'red']
        pd_data = pd.DataFrame([sname + wdata + slope + pcolor], columns=header)
        borrow_data = borrow_data.append(pd_data)

path = '../Data/'+str(year)+'Final_Wavelet_Trend(Return).txt'
with open(path, 'r', encoding='utf-8') as file_handle:
    for line in file_handle.readlines():
        field = line.split('|')
        sname = list(make_tuple(field[0]))
        wdata = list(make_tuple(field[1]))
        slope = [(wdata[0] - wdata[-1]) / (0 - len(wdata))]
        pcolor = ['blue' if slope[0] > 0 else 'red']
        pd_data = pd.DataFrame([sname + wdata + slope + pcolor], columns=header)
        return_data = return_data.append(pd_data)
# print(borrow_data.head())
# print(return_data.head())

all_borrow_data = pd.merge(ubike_slice, borrow_data, on='sna')
all_return_data = pd.merge(ubike_slice, return_data, on='sna')

# 正規化 slope 數值
borrow_slope = all_borrow_data.loc[:, 'slope'].values
scaler = MinMaxScaler()
norm_slope = scaler.fit_transform(borrow_slope.reshape(-1, 1))
all_borrow_data = pd.concat((all_borrow_data, pd.DataFrame(norm_slope, columns=['norm slope'])), axis=1)

return_slope = all_return_data.loc[:, 'slope'].values
scaler2 = MinMaxScaler()
norm_slope = scaler2.fit_transform(return_slope.reshape(-1, 1))
all_return_data = pd.concat((all_return_data, pd.DataFrame(norm_slope, columns=['norm slope'])), axis=1)

print(all_borrow_data.head())
print(all_return_data.head())

# 先做借用的圖在座歸還的圖
# 台北車站 (25.049034, 121.514252)
center = [25.049034, 121.514252]
for condition in ['Borrow', 'Return']:
    if condition == 'Borrow':
        lat = all_borrow_data.loc[:, 'lat'].values
        lng = all_borrow_data.loc[:, 'lng'].values
        text = all_borrow_data.loc[:, 'sna'].values
        color = all_borrow_data.loc[:, 'color'].values
        opacity = all_borrow_data.loc[:, 'norm slope'].values

    else:
        lat = all_return_data.loc[:, 'lat'].values
        lng = all_return_data.loc[:, 'lng'].values
        text = all_return_data.loc[:, 'sna'].values
        color = all_return_data.loc[:, 'color'].values
        opacity = all_return_data.loc[:, 'norm slope'].values

    data = [
        go.Scattermapbox(
            lat=lat,
            lon=lng,
            mode='markers',
            marker=dict(
                size=opacity*25,
                color=color,
                opacity=opacity
            ),
            text=text
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=center[0],
                lon=center[1]
            ),
            pitch=0,
            zoom=10
        ),
    )

    fig = dict(data=data, layout=layout)
    py.iplot(fig, filename='Taipei Ubike Station')
    x = input('<---Enter Something to show fig--->')
