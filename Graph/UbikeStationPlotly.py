import pandas as pd
import numpy as np
import plotly
import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go

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
print('ubike_station\n', ubike_station.head())

# 台北車站 (25.049034, 121.514252)
ubike_station_latitude = ubike_station.loc[:, 'lat'].values
ubike_station_longitude = ubike_station.loc[:, 'lng'].values
ubike_station_name = ubike_station.loc[:, 'sna']
print(ubike_station_latitude)
print(ubike_station_longitude)

center = [25.049034, 121.514252]
data = [
    go.Scattermapbox(
        lat=ubike_station_latitude,
        lon=ubike_station_longitude,
        mode='markers',
        marker=dict(
            size=9,
            color='red'
        ),
        text=ubike_station_name
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
