"""
Name: Kar Yeung Ng
CS230: Section 2
Data: Boston AirBnB Listing

Description:
This project includes 2 graphs and 4 filters for users to choose their favorable AirBnBs. The 2 graphs include an
interactive map that will show the location of the AirBnBs base on the filters, and a bar chart that will compare the
amount of listings base on the chosen neighbourhoods. The 4 filters include neighbourhood, price, nights of stay, and
the type of rooms AirBnB users are looking for. The purpose of this web application is to make the AirBnB selection in
the Boston area a more convenient process.
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk


DIR = 'airbnb.csv'

#reading excel file
def read_data(filename):
    df = pd.read_csv(filename)
    lst = []
    columns = ['name', 'neighbourhood', 'latitude', 'longitude', 'price', 'minimum_nights', 'room_type']
    for index, row in df.iterrows():
        sub = []
        for col in columns:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)
    return lst

#creating neighbourhood data
def neighbourhoods_list(data):
    neighbourhoods = []
    for i in range(len(data)):
        if data[i][1] not in neighbourhoods:
            neighbourhoods.append(data[i][1])
    return neighbourhoods

#creating room type data
def room_type_list(data):
    room_types = []
    for i in range(len(data)):
        if data[i][6] not in room_types:
            room_types.append(data[i][6])
    return room_types


def freq_data(data, neighbourhoods, price):
    freq_dict = {}
    for neighbourhood in neighbourhoods:
        frequency = 0
        for i in range(len(data)):
            if data[i][1] == neighbourhood and price >= data[i][4]:
                frequency += 1
        freq_dict[neighbourhood] = frequency
    return freq_dict

#making bar chart
def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()

    plt.bar(x, y)
    plt.xticks(rotation=25)
    plt.xlabel('Neighbourhood')
    plt.ylabel('Number of Listing')
    title = 'Listings Selected In'
    for key in freq_dict.keys():
        title += ", " + key
    plt.title(title)

    return plt

#making map
def display_map(data, neighbourhoods, price, min_night, room_type):
    loc = []
    for i in range(len(data)):
        if data[i][1] in neighbourhoods and price >= data[i][4] and min_night >= data[i][5] and data[i][6] in room_type: #interactive filters
            loc.append([data[i][0], data[i][2], data[i][3]])

    map_df = pd.DataFrame(loc, columns=['Listing', 'lat', 'lon'])

    view_state = pdk.ViewState(latitude=map_df['lat'].mean(), longitude=map_df['lon'].mean(), zoom=10, pitch=0)
    layer = pdk.Layer('ScatterplotLayer', data=map_df, get_position='[lon, lat]', auto_highlight=True, get_radius=25, get_color=[180, 0, 200, 140], pickable=True)
    tool_tip = {'html': 'Listing:<br/>{Listing}', 'style:': {'backgroundColor': 'blue', 'color': 'white'}}

    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer], tooltip=tool_tip)

    st.pydeck_chart(map)

#main page presentation
def main():
    data = read_data(DIR)

    st.title('Boston AirBnB Listings')
    st.write('Welcome! Please Select Your Neighbourhood, Price, and Nights for Stay.')

    neighbourhoods = st.sidebar.multiselect('Select neighbourhoods', neighbourhoods_list(data))
    pricelimit = st.sidebar.slider('Set price limit', 25.00, 2000.00, 150.00)
    min_night = st.sidebar.slider('Nights', 1, 300, 25)
    room_type = st.sidebar.multiselect('Select Room Type', room_type_list(data))

    if len(neighbourhoods) > 0:
        st.write('Listing Map')
        display_map(data, neighbourhoods, pricelimit, min_night, room_type)
        st.write('\nTotal Listing Counts')
        st.pyplot(bar_chart(freq_data(data, neighbourhoods, pricelimit)))


main()
