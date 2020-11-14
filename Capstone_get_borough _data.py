#!/usr/bin/env python
# coding: utf-8

# In[26]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 


from IPython.display import display_html
import pandas as pd
import numpy as np
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

#!conda install -c conda-forge folium=0.5.0 --yes
get_ipython().system('pip install folium')
import folium # plotting library
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
import matplotlib.cm as cm
import matplotlib.colors as colors

print('Folium installed')
print('Libraries imported.')


# In[27]:


source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup=BeautifulSoup(source,'lxml')
print(soup.title)
from IPython.display import display_html
tab = str(soup.table)
display_html(tab,raw=True)


# I replaces Not assigned with a nan value and then dropped for boroughs and filled the neighboorhood names.
# 
# Next, I will conbine neighboorhoods with the same postal code as required

# In[28]:



dfs = pd.read_html(tab)
df=dfs[0]
df.head()


# In[29]:


# Dropping the rows where Borough is 'Not assigned'
df1 = df[df.Borough != 'Not assigned']

# Combining the neighbourhoods with same Postalcode
df2 = df1.groupby(['Postal Code','Borough'], sort=False).agg(', '.join)
df2.reset_index(inplace=True)

# Replacing the name of the neighbourhoods which are 'Not assigned' with names of Borough
df2['Neighbourhood'] = np.where(df2['Neighbourhood'] == 'Not assigned',df2['Borough'], df2['Neighbourhood'])

df2


# In[30]:


df2.shape


# In[31]:



lat_lon = pd.read_csv('https://cocl.us/Geospatial_data')
lat_lon.head()


# In[32]:


df3 = pd.merge(df2,lat_lon,on='Postal Code')
df3.head()


# In[ ]:




