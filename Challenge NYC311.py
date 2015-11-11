
# coding: utf-8

# In[54]:

from __future__ import division

import pandas as pd
import numpy as np
import graphlab as gl
import time

from datetime import datetime

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')


# In[2]:

columns_of_interest = ['Created Date', 'Agency', 'Complaint Type', 'Borough', 'Latitude', 'Longitude']


# In[3]:

# uncomment for the first run

# # only load necessary columns to save space
# sf = gl.SFrame.read_csv('nyc311calls.csv', verbose = False, usecols = columns_of_interest)

# # save to binary for fast future access
# sf.save('nyc311_sframe')


# In[4]:

sf = gl.load_sframe('nyc311_sframe')
num_complaints = len(sf)
sf


# # Question 1

# In[5]:

complaints_by_agency = sf.groupby(key_columns = 'Agency', operations = {'Count': gl.aggregate.COUNT()})


# In[6]:

complaints_by_agency = complaints_by_agency.sort('Count', ascending = False)
complaints_by_agency


# In[7]:

print 'Fraction of complaints are associated with the 2nd most popular agency:'
print complaints_by_agency['Agency'][1], complaints_by_agency['Count'][1] / len(sf)


# # Question 2

# In[8]:

complaints_by_type = sf.groupby(key_columns = 'Complaint Type',
                                operations = {'Count of Type': gl.aggregate.COUNT()})
complaints_by_type


# In[9]:

complaints_by_borough = sf.groupby(key_columns = 'Borough',
                                   operations = {'Count of Borough': gl.aggregate.COUNT()})
complaints_by_borough


# In[10]:

complaints_by_borough_type = sf.groupby(key_columns = ['Borough', 'Complaint Type'],
                                        operations = {'Count of Borough and Type': gl.aggregate.COUNT()})
complaints_by_borough_type


# In[11]:

complaints_by_borough_type = complaints_by_borough_type.join(complaints_by_borough,
                                                             on=['Borough'], how = 'outer')
complaints_by_borough_type = complaints_by_borough_type.join(complaints_by_type,
                                                             on=['Complaint Type'], how = 'outer')
complaints_by_borough_type


# In[12]:

complaints_by_borough_type['Pr(Type)'] = complaints_by_borough_type.apply(lambda x:
                                         x['Count of Type'] / num_complaints)

complaints_by_borough_type['Pr(Type | Borough)'] = complaints_by_borough_type.apply(lambda x:
                                                   x['Count of Borough and Type'] / x['Count of Borough']) 

complaints_by_borough_type['Surprise'] = complaints_by_borough_type.apply(lambda x:
                                                   x['Pr(Type | Borough)'] / x['Pr(Type)'])
complaints_by_borough_type


# In[13]:

complaints_by_borough_type.sort('Surprise', ascending = False)['Complaint Type'][0]


# # Question 3

# In[14]:

lat_90 = np.percentile(sf['Latitude'], 90)
lat_10 = np.percentile(sf['Latitude'], 10)


# In[15]:

lat_90 - lat_10


# # Question 4

# In[16]:

# I am doing flat surface approximation, because:
# a) I am calculating _approximate_ area to begin with
# b) area is small, so the Earth curvature is negligible
# conversion numbers from Wikipedia, take ellipticity of Earth into account

mean_latitude = sf['Latitude'].mean()

km_in_latitude_degree = 110.574
km_in_longitude_degree = 111.320 * np.cos( np.radians(mean_latitude) )


# In[17]:

std_latitude_km  = sf['Latitude'].std() * km_in_latitude_degree
std_longitude_km = sf['Longitude'].std() * km_in_longitude_degree


# In[18]:

area = 0.25 * np.pi * std_latitude_km * std_longitude_km
area


# # Question 5

# In[98]:

date_format = '%m/%d/%Y %I:%M:%S %p'

sf['Time'] = sf['Created Date'].apply(lambda x : datetime.strptime(x, date_format))
sf['Hour'] = sf['Time'].apply(lambda x : int(x.hour))
sf['Time'] = sf['Time'].apply( lambda x : int(time.mktime( x.timetuple() )) )


# In[99]:

time = np.array(sf['Time'])
diff = np.append(np.diff(time), [0])

# keep only times for which difference with previous time is between -1000 and 0 seconds (non-inclusive)
sf['Time Difference'] = diff
sf['Good Time'] = np.logical_and(np.greater(diff, -1000), np.less(diff, 0))


# In[100]:

sf


# In[101]:

complaints_by_hour = sf[sf['Good Time'] == 1].groupby(key_columns = 'Hour',
                                                      operations = {'Count': gl.aggregate.COUNT()})
complaints_by_hour


# In[102]:

complaints_by_hour['Count'].max() - complaints_by_hour['Count'].min()


# # Question 6

# In[105]:

sf['Time Difference'][sf['Good Time'] == 1].std()


# In[ ]:



