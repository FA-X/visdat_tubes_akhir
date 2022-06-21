# -*- coding: utf-8 -*-
"""tubes_visdat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ja__g9TgzSdj0fPREBY6bhig7vADdk1j

#Define library yang digunakan
"""

#install pyproj
!pip install pyproj
#define library
from bokeh.io import curdoc
from pyproj import Proj, transform
import pandas as pd
import datetime as dt
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, gridplot
from bokeh.models import Slider, Select
from bokeh.models import DatePicker, Select, ColumnDataSource, ColorBar
from bokeh.palettes import Spectral6
from bokeh.models import CategoricalColorMapper
from bokeh.transform import linear_cmap
from bokeh.layouts import widgetbox, row, column, gridplot
from bokeh.plotting import figure
from bokeh.tile_providers import get_provider, WIKIMEDIA, CARTODBPOSITRON, STAMEN_TERRAIN, STAMEN_TONER, ESRI_IMAGERY, OSM

import warnings

"""#Import dataset"""

#Download dataset
# !gdown --id 1xmiMcvvfxVVTK3Rft536AGpB5l38EdUN

#import dataset
data = pd.read_csv("./covid-19_data.csv")
#mengubah kolom date jadi dataset
data.set_index('Date', inplace=True)

data.head(5)

"""#Define cartodbpositron"""

#define beberapa variabel untuk membuat peta dengan cartodbpositron
inProj = Proj(init='epsg:3857')
outProj = Proj(init='epsg:4326')

ind_lon1, ind_lat1 = transform(outProj,inProj,90,-15)
ind_lon2, ind_lat2 = transform(outProj,inProj,150,20)
cartodb = get_provider(CARTODBPOSITRON)

"""#Membuat source data dengan ColumDataSource"""

#define variabel 'df' dengan data pada tanggal 2020-03-01 
df = data[data.index == '2020-03-01']

#define variabel nam untuk menampung nama kolom yang di select
nam = []
for i in df.new_cases:
    nam.append("new_cases")

#source digunakan untuk menampilkan data yang akan ditampilkan (data awal)
source = ColumnDataSource(data={
    'x'         : df.MercatorX, #define x dengan kolom mercatorX dari data dengan index tanggal 2020-03-01
    'y'         : df.MercatorY, #define y dengan kolom mercatorY dari data dengan index tanggal 2020-03-01
    'dat'       : df.new_cases, #define dat dengan kolom new_cases dari data dengan index tanggal 2020-03-01
    'nama'      : nam #define nama dengan nama kolom new_cases 
})

"""#Mapper color, define figure (map), dan define scatterplot(circle)"""

#mapper adalah list color dimana akan berwarna merah jika nilai dari data sekitar 800000 dan berwarna biru jika bernilai mendekati 0
mapper = linear_cmap('dat', Spectral6 , 0 , 849875)

#menampilkan peta pada visualisasi data
p = figure(plot_width=900, plot_height=700,
           x_range=(ind_lon1, ind_lon2), y_range=(ind_lat1, ind_lat2),
           x_axis_type="mercator", y_axis_type="mercator",
           tooltips=[
                    ("Data", "@nama"), ("Jumlah", "@dat") #menampilkan data tiap kolom/data yang diselect
                    ],
           title="Covid in Indonesia")

p.add_tile(cartodb)
#plotting scatter plot (circle)
p.circle(x='x', y='y',
         size=10,
         line_color=mapper, color=mapper,
         fill_alpha=1.0,
         source=source)
#menampilkan color bar
color_bar = ColorBar(color_mapper=mapper['transform'], width=8)

p.add_layout(color_bar, 'right')

"""#Function update plot dan data"""

def update_plot(attr, old, new):
    df = data[data.index == str(dPicker.value)] #update 'df' dengan data dari index date yang di select oleh fitur datepicker
    nam = []
    for i in df.new_cases:
        nam.append(str(data_select.value)) #update var nam
    source.data = {
        'x'         : df.MercatorX, #update x dengan kolom mercatorX dari data index date yang di select oleh fitur datepicker
        'y'         : df.MercatorY, #define y dengan kolom mercatorY dari data index date yang di select oleh fitur datepicker
        'dat'       : df[data_select.value], #update dat dengan kolom new_cases dari data kolom yang diselect pada fitur dropdwon select
        'nama'      : nam #update nama dengan nama kolom sesuai dengan kolom yang diselect
    }

"""#Define fitur interaktif"""

#define fitur interaktif date picker
dPicker = DatePicker(
    title = 'Date',
    value=dt.datetime(2020, 3, 1).date(), 
    min_date= dt.datetime(2020, 3, 1).date(), max_date=dt.datetime(2021, 12, 3).date()
)

dPicker.on_change('value', update_plot)

#define fitur interaktif dropdown dan select
data_select = Select(
    options=['new_cases', 'new_deaths',	'new_recovered', 'new_activeCases', 'total_cases', 'total_deaths',	'total_recovered', 'total_activeCases'],
    value='new_cases',
    title='x-axis data'
)

data_select.on_change('value', update_plot)

"""#Membuat layout"""

#memasukan seluruh fitur interaktif dan juga plotingan kedalam layout
layout = row(widgetbox(dPicker, data_select), p) 
curdoc().add_root(column(layout))

"""#Penjelasan



1.   Alasan kami menggunakan DatePicker dibanding menggunakan slide adalah karna data yang kami gunakan adalah data per-hari dalam rentang 2020-2021 sehingga apabila menggunakan slider untuk memilih tanggal hal tersebut tidak efisien dan sulit untuk memilih tanggal tertentu
2.   Alasan kami melakukan visualisasi dalam geospatial/map interaktif dibanding tipe visualisasi lain seperti scatter atau line adalah 

      *   data yang kami miliki merupakan data per-provinsi dengan jumlah data yang sangat banyak
      *   jika dilihat pada kolom date terdapat data yang berbeda dengan tanggal yang sama (dalam satu tanggal misal 2021-07-17 terdapat data yang berbeda dari daerah yang berbeda juga

 sehingga bentuk dari visualisasi dengan scatter atau line plot kurang memberikan isi dari visualisasi dataset covid. Jika menggunakan map catodbpositron ini maka kami akan mendapatkan visualisasi daerah mana saja yang terdampak covid dengan intensitas yang tinggi dan rendah, selain itu juga memudahkan kita mendapatkan insight dengan tipe visualisasi seperti ini


"""
