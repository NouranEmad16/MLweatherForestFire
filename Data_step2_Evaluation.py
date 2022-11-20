#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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


# In[5]:


# tableName = "public.\"dbfNFDB_poin\""
# table_df = gpd.read_postgis("SELECT * FROM " + tableName, db_con)
tableName = "public.\"dbfNFDB_poin\""
table_df = pd.read_sql("SELECT * FROM " + tableName, db_con)


# In[6]:


table_df.head()


# In[7]:


table_df.describe()


# In[ ]:




