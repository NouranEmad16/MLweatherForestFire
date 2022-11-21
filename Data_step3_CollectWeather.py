#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#%pip install rtree
#%pip install pygeos


# In[1]:


import os
import sys
import pandas as pd
import geopandas as gpd
import pygeos as pg
import tensorflow as tf
import sqlalchemy as sq
import ipyparallel as ipp
from matplotlib import pyplot as plt
import ClimateDataRequester as cdr

# The following lines adjust the granularity of reporting. 
pd.options.display.max_rows = 10
pd.options.display.float_format = "{:.1f}".format
pd.set_option('display.max_columns', None)
os.chdir('/tf')


# In[2]:


db_connection_url = "postgresql://grpthreeuser:grpthreeuser@postgres:5432/grpthreedb"
engine = sq.create_engine(db_connection_url)
db_con = engine.connect()


# In[3]:


tableName = "public.\"lgFireFifty\""
query = "SELECT * FROM " + tableName + " WHERE \"YEAR\" > 2009;"
table_df = gpd.GeoDataFrame.from_postgis(query, db_con)


# In[4]:


dfIDgeom = table_df[['EntryID', 'geom']]
dfIDgeom.head()


# In[5]:


# create df of weather station locations

dfStationsRaw = pd.read_csv('Data/climate_station_list.csv')
dfStationsRaw.head()


# In[6]:


dfStations = dfStationsRaw[['Station Name', 'Latitude', 'Longitude', 'Climate ID', 'DLY First Year', 'DLY Last Year']]
dfStations.head()


# In[7]:


dfStations.describe()


# In[8]:


# first we prune by year
dfStations = dfStations.loc[dfStations['DLY Last Year'] > 2009]
dfStations.describe()


# In[9]:


# create a geom point column
dfStations['geom'] = gpd.points_from_xy(dfStations['Longitude'], dfStations['Latitude'])
gdfStations = gpd.GeoDataFrame(dfStations, crs=4326, geometry='geom')
gdfStations.head()


# In[10]:


# get provincial boundaries
dfProvinces = gpd.GeoDataFrame.from_postgis("SELECT * FROM " + "public.\"dbfProvBound\"", db_con)


# In[11]:


# this normally takes 90s to run
f, ax = plt.subplots(figsize=(19.20, 10.80))
dfProvinces.to_crs(3978).boundary.plot(ax=ax, color=None, edgecolor='black', linewidth=1)
gdfStations.to_crs(3347).plot(ax=ax, color='red', markersize=0.3)
dfIDgeom.to_crs(3347).plot(ax=ax, color='blue', alpha=0.5)


# In[27]:


# project to same crs
gdfStations = gdfStations.to_crs(3347)
dfIDgeom = dfIDgeom.to_crs(3347)

# match station to nearesat fire within 150km
dfResult = gpd.sjoin_nearest(left_df=gdfStations, right_df=dfIDgeom, how='left' , max_distance=150000, distance_col='distance') 
dfResult.head()


# In[28]:


# remove stations that are not within 150km of a fire
dfResult = dfResult.loc[dfResult['EntryID'].notnull()]
dfResult.head()


# In[30]:


# keep interesting columns
dfResult = dfResult[['Station Name', 'Climate ID', 'DLY First Year', 'DLY Last Year', 'distance', 'geom']]
dfResult.describe()


# In[31]:


# push to db
dfResult.set_crs(3347)
dfResult.to_postgis("lgFireStationsTen", db_con, index=False, if_exists='replace')


# In[33]:


# dfProvinces = dfProvinces.to_crs(3978)
# dfProvinces.set_crs(3347, allow_override=True)
# dfProvinces.to_postgis("dbfProvBound", db_con, index=False, if_exists='replace')


# In[35]:


# tableName = "public.\"lgFireFiftyCentroids\""
# query = "SELECT * FROM " + tableName + ";"
# dfLgFiresCentroids = gpd.GeoDataFrame.from_postgis(query, db_con)

# dfLgFiresCentroids = dfLgFiresCentroids.to_crs(3347)
# dfLgFiresCentroids.set_crs(3347)
# dfLgFiresCentroids.to_postgis("lgFireFiftyCentroids", db_con, index=False, if_exists='replace')


# In[36]:


# tableName = "public.\"lgFireFifty\""
# query = "SELECT * FROM " + tableName + ";"
# dfLgFires = gpd.GeoDataFrame.from_postgis(query, db_con)

# dfLgFires = dfLgFires.to_crs(3347)
# dfLgFires.set_crs(3347)
# dfLgFires.to_postgis("lgFireFifty", db_con, index=False, if_exists='replace')

