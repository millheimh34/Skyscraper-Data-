'''
Project by: Hogan Millheim
Data: Skyscrapers
Description: This app allows users to visualize skyscraper data. They can select a city for which
they would like to see skyscrapers and the material the skyscraper is made of. They can also view
in a map where all skyscrapers are located around the world. There is section where the user can see
the completion date and which skyscrapers were completed in that date.
'''

import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
from matplotlib.backends.backend_agg import RendererAgg
from streamlit_folium import st_folium
import folium



def get_skyscraper_data():
   # return pd.read_csv(os.path.join(os.getcwd(), 'Skyscrapers2021V2.csv'))
    return pd.read_csv('Skyscrapers2021V2.csv', index_col=0)

st.set_page_config(layout="wide")
df_sky = get_skyscraper_data()

st.title('SkyScraper Data Visualization Tool')
st.markdown("""
This app shows detailed skyscraper data.
""")

st.header("Data Table of Selected City and Material")

st.sidebar.header('Choose What to Display')
skyscraper_data = df_sky
City = df_sky['CITY'].unique().tolist()
Completion = df_sky['COMPLETION'].unique().tolist()
Height = df_sky['Height'].tolist()
Meters = df_sky['Meters'].unique().tolist()
Feet = df_sky['Feet'].unique().tolist()
Floors = df_sky['FLOORS'].unique().tolist()
Material = df_sky['MATERIAL'].unique().tolist()
Function = df_sky['FUNCTION'].unique().tolist()

skyscraper_selected = st.sidebar.multiselect('Select City', City, City)
skyscraper_selected2 = st.sidebar.multiselect('Select Building Material', Material, Material)

mask_City = df_sky['CITY'].isin(skyscraper_selected)
mask_Completion = df_sky['COMPLETION'].isin(skyscraper_selected)
mask_Height = df_sky['Height'].isin(skyscraper_selected)
mask_Meters = df_sky['Meters'].isin(skyscraper_selected)
mask_Feet = df_sky['Feet'].isin(skyscraper_selected)
mask_Floors = df_sky['FLOORS'].isin(skyscraper_selected)
mask_Material = df_sky['MATERIAL'].isin(skyscraper_selected2)
mask_Function = df_sky['FUNCTION'].isin(skyscraper_selected)

def_sky_filtered = df_sky[mask_City & mask_Material]

st.write(def_sky_filtered)

matplotlib.use("agg")
_lock = RendererAgg.lock

city_counts = def_sky_filtered['CITY'].value_counts()

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.2, 1, .2, 1, .2))

with row0_1, _lock:
    st.header("Skyscraper Count in Each City")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(city_counts, labels=(city_counts.index + ' (' + city_counts.map(str)
                                + ')'), wedgeprops={'linewidth': 7, 'edgecolor': 'white'
                                                    }, colors='b')
    # display a white circle in the middle of the pie chart
    p = plt.gcf()
    p.gca().add_artist(plt.Circle((0, 0), 0.7, color='white'))
    st.pyplot(fig)

material_counts = def_sky_filtered['MATERIAL'].value_counts()

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((0.2, 1, .2, 1, .2))

with row0_1, _lock:
    st.header("Material Count of Skyscrapers ")
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(material_counts, labels=(material_counts.index + ' (' + material_counts.map(str)
                                    + ')'), wedgeprops={'linewidth': 7, 'edgecolor': 'white'
                                                        }, colors='g')

    p = plt.gcf()
    p.gca().add_artist(plt.Circle((0, 0), 0.7, color='white'))
    st.pyplot(fig)

df = pd.read_csv("Skyscrapers2021V2.csv", usecols=['Feet', 'FLOORS'])
fig = px.scatter(df,
                 x="Feet",
                 y="FLOORS",
                 )
st.header("Height of Building to Number of Floors")

st.plotly_chart(fig)

st.header("Map for Viewing Location of Skyscrapers")

mymap = folium.Map(location=[1.366623, 103.821285], width=950, height=550, zoom_start=2, tiles='Stamen Terrain')
folium.TileLayer('Stamen Toner').add_to(mymap)
folium.TileLayer('Stamen Water Color').add_to(mymap)
folium.LayerControl().add_to(mymap)
for lat, lng, Name in zip(df_sky['Latitude'], df_sky['Longitude'], df_sky['NAME']):
    skyscraper = folium.Marker(location=[lat, lng], popup=Name, )
    skyscraper.add_to(mymap)

st_folium(mymap)

st.header('List of Skyscrapers and Year of Completion')

col_name = 'COMPLETION'

for name, group in df_sky.groupby([col_name]):

    st.write(name, group)

# df_sky['Height'].pyplot(kind='box',title='Skyscraper Heights')

# st.pyplot

'''
References:

https://medium.com/@max.lutz./how-to-build-a-data-visualization-page-with-streamlit-4ca4999eba64

https://pythonwife.com/introduction-to-streamlit/

https://towardsdatascience.com/visualization-in-python-visualizing-geospatial-data-122bf85d128f

'''
