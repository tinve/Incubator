
# coding: utf-8

# In[1]:

from __future__ import division

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

get_ipython().magic(u'matplotlib inline')


# In[2]:

df = pd.read_csv('Crimes_-_2001_to_present.csv')

date_format = '%m/%d/%Y %I:%M:%S %p'
df['Date'] = df['Date'].apply(lambda x : datetime.strptime(x, date_format))

df['Year'] = df['Date'].apply(lambda x : x.year)

df.head()


# In[3]:

df.info()


# In[4]:

df.dtypes


# In[5]:

df.count()


# In[27]:

sns.factorplot(x = 'Arrest', data = df, kind = "count")


# In[47]:

years = np.arange(2001, 2015)
g = sns.factorplot(x = "Year", data = df, kind = "count",
                   palette = "BuPu", size = 6, aspect = 1.5, order = years)


# In[6]:

by_description = df[['Location Description', 'ID']].groupby('Location Description').agg('count').sort('ID', ascending = False)


# In[7]:

by_description[:10].index


# In[21]:

width = .35
ind = np.arange(10)
plt.bar(ind, list(by_description[:10]['ID']))
plt.xticks(ind + width / 2, by_description[:10].index, rotation = 45)

# fig.autofmt_xdate()

# plt.savefig("figure.pdf")


# In[18]:

list(by_description[:10]['ID'])


# In[ ]:



