#!/usr/bin/env python
# coding: utf-8

# #Group3_Data_Operations

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


# In[ ]:


def pushToPostGresDB(fi):
    import geopandas as gpd
    import sqlalchemy as sq
    
    db_connection_url = "postgresql://grpthreeuser:grpthreeuser@postgres:5432/grpthreedb"
    db_con = sq.create_engine(db_connection_url)

    geodf = gpd.read_file(fi, encoding="utf-8")
    geodf = geodf.set_crs(3978, allow_override=True)
    tableName = fi[-3:]+fi[fi.find("/")+1:fi.find("_")+5]
    
    geodf.to_postgis(tableName, db_con, index=False, if_exists='replace')
    return fi
            
            


# In[ ]:


#create a list of full path file names from directory
def getFileList():
    DATA_DIR = "Data/"
    fullPathNames = []
    for fi in os.listdir(DATA_DIR):
        fi = os.path.join(DATA_DIR, fi)
        if os.path.isfile(fi):
            if fi.endswith("dbf") or fi.endswith("shp") :
                fullPathNames.append(fi)
    return fullPathNames


# In[ ]:


#set up parallel computing cluster
cluster = ipp.Cluster.from_file("/root/.ipython/profile_default/security/cluster-.json")
rc = cluster.connect_client_sync()
rc


# In[ ]:


# cluster = ipp.Cluster(n=4)
# await cluster.start_cluster()
# rc = cluster.connect_client_sync()
rc.wait_for_engines(n=4)
dview = rc[:]
dview.block=True



# In[ ]:


# transfer to postgres go brr
files = getFileList()
result = dview.map_sync(pushToPostGresDB, files)
print(result)


# In[ ]:


#uncomment to install more modules
#%pip install geoalchemy2


#uncomment the next 2 to see all installed modules
# import os
# os.system("pip list")

