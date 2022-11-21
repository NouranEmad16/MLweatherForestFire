#!/usr/bin/env python
# coding: utf-8

# In[1]:


#@title Import relevant modules
import os
import sys
import pandas as pd
import geopandas as gpd
import tensorflow as tf
import sqlalchemy as sq
import ipyparallel as ipp
from matplotlib import pyplot as plt

# The following lines adjust the granularity of reporting. 
pd.options.display.max_rows = 10
pd.options.display.float_format = "{:.1f}".format


# In[2]:


db_connection_url = "postgresql://grpthreeuser:grpthreeuser@postgres:5432/grpthreedb"
engine = sq.create_engine(db_connection_url)
db_con = engine.connect()


# In[3]:


# tableName = "public.\"dbfNFDB_poin\""
# table_df = gpd.read_postgis("SELECT * FROM " + tableName, db_con)
tableName = "public.\"lgFireFifty\""
table_df = gpd.GeoDataFrame.from_postgis("SELECT * FROM " + tableName, db_con)


# In[4]:


pd.set_option('display.max_columns', None)
table_df.head()


# In[5]:


table_df.describe()


# In[7]:


dfSelectColumns = table_df
dfSelectColumns.head()


# In[8]:


dfSelectColumns.describe()


# In[9]:


#dfSelectColumns.plot()


# In[12]:


# get provincial boundaries
dfProvinces = gpd.GeoDataFrame.from_postgis("SELECT * FROM " + "public.\"dbfProvBound\"", db_con)


# In[21]:


# this normally takes 90s to run
f, ax = plt.subplots(figsize=(19.20, 10.80))
dfProvinces.to_crs(3978).boundary.plot(ax=ax, color=None, edgecolor='black', linewidth=1)
dfSelectColumns.to_crs(3347).plot(ax=ax, color='red')


# In[23]:


dfCentroids = dfSelectColumns[['EntryID', 'geom']].copy()
dfCentroids['geom'] = dfSelectColumns['geom'].centroid


# In[25]:


f2, ax2 = plt.subplots(figsize=(19.20, 10.80))
dfProvinces.to_crs(3978).boundary.plot(ax=ax2, color=None, edgecolor='black', linewidth=1)
dfCentroids.to_crs(3347).plot(ax=ax2, color='red', markersize=0.1)


# In[28]:


# run this once to push the data to the database
#dfCentroids.to_postgis("lgFireFiftyCentroids", db_con, index=False, if_exists='replace')

