# -*- coding: utf-8 -*-

from bokeh.io import curdoc
from pyproj import Proj, transform
import pandas as pd
import datetime as dt
from bokeh.models import DatePicker, Select, ColumnDataSource, ColorBar
from bokeh.palettes import Spectral6
from bokeh.transform import linear_cmap
from bokeh.layouts import widgetbox, row
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, WIKIMEDIA, CARTODBPOSITRON, STAMEN_TERRAIN, STAMEN_TONER, ESRI_IMAGERY, OSM

import warnings

data = pd.read_csv('./data/data_covid-19_indonesia.csv')
data.set_index('Date', inplace=True)

inProj = Proj(init='epsg:3857')
outProj = Proj(init='epsg:4326')

ind_lon1, ind_lat1 = transform(outProj,inProj,90,-15)
ind_lon2, ind_lat2 = transform(outProj,inProj,150,20)
cartodb = get_provider(CARTODBPOSITRON)

df = data[data.index == '2020-03-01']

nam = []
for i in df.new_cases:
    nam.append("new_cases")

source = ColumnDataSource(data={
    'x'         : df.MercatorX,
    'y'         : df.MercatorY,
    'dat'       : df.new_cases,
    'nam'      : df.Province,
    'dit'       : df.Island
})

mapper = linear_cmap('dat', Spectral6 , 0 , 849875)


plot = figure(plot_width = 700, 
              plot_height = 500,
              x_range = (ind_lon1, ind_lon2), 
              y_range = (ind_lat1, ind_lat2),
              x_axis_type = "mercator", 
              y_axis_type = "mercator",
              tooltips = [
                    ("Provinsi", "@nam"),
                    ("Jumlah", "@dat"), 
                    ("Pulau", "@dit")
                    ],
             title="Covid19 di Indonesia")

plot.add_tile(cartodb)

plot.circle(x='x', y='y',
         size=8,
         line_color=mapper, color=mapper,
         fill_alpha=1.0,
         source=source)

color_bar = ColorBar(color_mapper=mapper['transform'], width=10)

plot.add_layout(color_bar, 'right')

def update_plot(attr, old, new):
    df = data[data.index == str(dPicker.value)]
    nam = []
    for i in df.new_cases:
        nam.append(str(select.value))
    source.data = {
        'x'         : df.MercatorX,
        'y'         : df.MercatorY,
        'dat'       : df[select.value],
        'nam'      : df.Province,
         'dit'       : df.Island
    }

dPicker = DatePicker(
    title = 'Date',
    value=dt.datetime(2020, 3, 1).date(),
    min_date= dt.datetime(2020, 3, 1).date(), 
    max_date=dt.datetime(2021, 12, 3).date()
)

dPicker.on_change('value', update_plot)

select = Select(
    options=['total_cases', 'total_deaths', 'total_recovered', 'total_activeCases', 'new_cases', 'new_deaths','new_recovered', 'new_activeCases'],
    value='new_cases',
    title='pilih data'
)

select.on_change('value', update_plot)

layout = row(widgetbox(dPicker, select), plot)
curdoc().add_root(layout)
