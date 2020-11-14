#!/usr/bin/env python
# coding: utf-8

# In[40]:



import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe
import folium # map rendering library

print('Libraries imported.')


# In[41]:


CLIENT_ID = 'Z2XZSS1ZQ0QAHF3Q1ZCZ1PEV245CQINXDA2FTY2YSOBQ0VBQ' # your Foursquare ID
CLIENT_SECRET = '4UN0IYUIGVSFHMINJXPR0TPV1XF43IRH1NKRCIM3JFPRZ4HI' # your Foursquare Secret
VERSION = '20180605' # Foursquare API version

print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)


# In[42]:


# type your answer here
LIMIT = 500 # Maximum is 100
cities = ["New York, NY", 'Chicago, IL', 'San Francisco, CA', 'Jersey City, NJ', 'Boston, MA']
results = {}
for city in cities:
    url = 'https://api.foursquare.com/v2/venues/explore?&client_id={}&client_secret={}&v={}&near={}&limit={}&categoryId={}'.format(
        CLIENT_ID, 
        CLIENT_SECRET, 
        VERSION, 
        city,
        LIMIT,
        "4bf58dd8d48988d1ca941735") # PIZZA PLACE CATEGORY ID
    results[city] = requests.get(url).json()


# In[43]:


df_venues={}
for city in cities:
    venues = json_normalize(results[city]['response']['groups'][0]['items'])
    df_venues[city] = venues[['venue.name', 'venue.location.address', 'venue.location.lat', 'venue.location.lng']]
    df_venues[city].columns = ['Name', 'Address', 'Lat', 'Lng']


# In[44]:


maps = {}
for city in cities:
    city_lat = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lat'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lat']])
    city_lng = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lng'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lng']])
    maps[city] = folium.Map(location=[city_lat, city_lng], zoom_start=11)

    # add markers to map
    for lat, lng, label in zip(df_venues[city]['Lat'], df_venues[city]['Lng'], df_venues[city]['Name']):
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(maps[city])  
    print(f"Total number of pizza places in {city} = ", results[city]['response']['totalResults'])
    print("Showing Top 100")


# In[45]:


maps[cities[0]]


# In[46]:


maps[cities[1]]


# In[47]:


maps[cities[2]]


# In[48]:


maps[cities[3]]


# In[49]:


maps[cities[4]]


# We can see that New York and Jersey City are the most dense cities with Pizza places. And better than that, they are just one shore away.
# 
# However, Let's have a concrete measure of this density.
# 
# For this I will use some basic statistics. I will get the mean location of the pizza places which should be near to most of them if they are really dense or far if not.
# 
# Next I will take the average of the distance of the venues to the mean coordinates.

# In[50]:


maps = {}
for city in cities:
    city_lat = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lat'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lat']])
    city_lng = np.mean([results[city]['response']['geocode']['geometry']['bounds']['ne']['lng'],
                        results[city]['response']['geocode']['geometry']['bounds']['sw']['lng']])
    maps[city] = folium.Map(location=[city_lat, city_lng], zoom_start=11)
    venues_mean_coor = [df_venues[city]['Lat'].mean(), df_venues[city]['Lng'].mean()] 
    # add markers to map
    for lat, lng, label in zip(df_venues[city]['Lat'], df_venues[city]['Lng'], df_venues[city]['Name']):
        label = folium.Popup(label, parse_html=True)
        folium.CircleMarker(
            [lat, lng],
            radius=5,
            popup=label,
            color='blue',
            fill=True,
            fill_color='#3186cc',
            fill_opacity=0.7,
            parse_html=False).add_to(maps[city])
        folium.PolyLine([venues_mean_coor, [lat, lng]], color="green", weight=1.5, opacity=0.5).add_to(maps[city])
    
    label = folium.Popup("Mean Co-ordinate", parse_html=True)
    folium.CircleMarker(
        venues_mean_coor,
        radius=10,
        popup=label,
        color='green',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(maps[city])

    print(city)
    print("Mean Distance from Mean coordinates")
    print(np.mean(np.apply_along_axis(lambda x: np.linalg.norm(x - venues_mean_coor),1,df_venues[city][['Lat','Lng']].values)))


# In[51]:


maps[cities[0]]


# In[52]:



maps[cities[1]]


# In[53]:



maps[cities[2]]


# In[54]:



maps[cities[3]]


# In[55]:



maps[cities[4]]


# 
# We now see that New York is his best option. And as aplus the Third best place is Jersey City which is just on the other side of the shore. 
# Our tourist's best interest would be to book a hotel near that mean coordinate to surround himself with the 100 Pizza stores there!!
# Another observation is that there is one really far away Pizza store which would possible increase its score to be beaten by New York
# So let's try to remove it and calculate it again

# In[57]:



city = 'Jersey City, NJ'
venues_mean_coor = [df_venues[city]['Lat'].mean(), df_venues[city]['Lng'].mean()] 

print(city)
print("Mean Distance from Mean coordinates")
dists = np.apply_along_axis(lambda x: np.linalg.norm(x - venues_mean_coor),1,df_venues[city][['Lat','Lng']].values)
dists.sort()
print(np.mean(dists[:-1]))# Ignore the biggest distance


# 
# That puts Jersey City back in the first place which makes our tourist happy.
# 
# Happy Pizza-rism!!
# And By that I conclude my Notebook
