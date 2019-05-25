import os
import gmplot
import numpy as np
import pandas as pd

from Method.LoadData import LoadData

desired_width = 320
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 20)

# Load ubike station
ubike_station = LoadData.load_ubike_station()
print('ubike_station\n', ubike_station.head())

# 台北車站 (25.049034, 121.514252)
ubike_station_latitude = ubike_station.loc[:, 'lat'].values
ubike_station_longitude = ubike_station.loc[:, 'lng'].values
print(ubike_station_latitude)
print(ubike_station_longitude)

center = [25.049034, 121.514252]
gmap = gmplot.GoogleMapPlotter(center[0], center[1], 13)
gmap.scatter(ubike_station_latitude, ubike_station_longitude, '#FF0000', size=40, marker=False)
rel_path = '../Data/Map/scatter.html'
gmap.draw(rel_path)

gheatmap = gmplot.GoogleMapPlotter(center[0], center[1], 13)
gheatmap.heatmap(ubike_station_latitude, ubike_station_longitude)
rel_path = '../Data/Map/heatmap.html'
gheatmap.draw(rel_path)



