#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("../")


import os
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from patsy import dmatrices
from openpyxl import load_workbook

data_path = start.data_path
table_path = start.table_path


# In[2]:


data = pd.read_csv(os.path.join(data_path, 'clean', 'master_data_district.csv'),
                  sep=",", low_memory= False)
data15 = data[data.year == 2015]
data18 = data[data['year'] == 2018]
data18.loc[:, 'eligible'] = np.where(((data18.rating_academic == 'D') | (data18.rating_academic == 'F')), False, True)
# Ignore charters
data18 = data18[data18.distischarter == "N"]


# In[3]:


len(data18)


# In[4]:


# Ineligible
len(data18[(data18.eligible == False) & (data18.doi == False)])


# In[5]:


# Number opting out
len(data18[((data18.eligible == True) & (data18.doi == False))])


# In[6]:


# DOIs
len(data18[data18.doi == True])


# In[7]:


data18.doi.value_counts()


# In[8]:


district_df = pd.DataFrame(data.groupby(['district']).agg({'doi_year': 'mean'}))
district_counts = pd.DataFrame(district_df.doi_year.value_counts(sort = False))
district_counts = district_counts.sort_index()
district_counts


# In[9]:


district_counts.doi_year.cumsum() 


# In[11]:


import matplotlib
plt.style.use('grayscale')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(['2015', '2016', '2017', '2018', '2019'], district_counts.doi_year.cumsum() , color = 'black')

plt.ylabel('Number of Districts')
#plt.title('Texas District of Innovation Takeup Over Time')
plt.xlabel('Test Year (Spring)', size = 'medium')
plt.grid(True, alpha = .6)


plt.ylim(0, 1022)
txt="Notes: Statistics are as of March 2019. There are ten Districts of Innovation (with missing Innovation Plans) \n that are not included in the figure. As of 2019, there were 1022 traditional public school districts in Texas."
plt.figtext(.5,-.01, txt, wrap=True, horizontalalignment='center', fontsize=8)

plt.savefig(table_path + 'takeup.png', dpi = 600, bbox_inches="tight")
plt.show()


# In[ ]:




