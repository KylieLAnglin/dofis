#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from cycler import cycler
from matplotlib import lines, markers
from scipy import stats

sys.path.append("../")
from library import start

# get_ipython().run_line_magic('matplotlib', 'inline')



# %%

data = pd.read_csv(os.path.join(start.data_path, 'clean', 'gdid_school.csv'),
                  sep=",", low_memory= False)
data[data.year == 2014].doi_year.value_counts().sort_index()


# %% Graph by Year of Implementation


def create_group_df(df):
    new_df = pd.DataFrame(df.groupby(['year']).agg({'avescores': ['mean', 'sem']}))
    new_df = new_df.rename(columns = {'mean': 'score_mean', 'sem': 'score_se'})
    new_df['ub'] = new_df['avescores']['score_mean'] + new_df['avescores']['score_se']
    new_df['lb'] = new_df['avescores']['score_mean'] - new_df['avescores']['score_se']
    return new_df
df_treat2017 = create_group_df(data[data.doi_year == 2017])
df_treat2018 = create_group_df(data[data.doi_year == 2018])
df_treat2019 = create_group_df(data[data.doi_year == 2019])
df_charter = create_group_df(data[data.distischarter == 'Y'])
df_treat2017


# %% Full Set of Years and Groups

plt.style.use('seaborn')
my_dpi = 96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)
years = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
# Pre
#plt.plot(list(df_charter.index), df_charter['avescores']['score_mean'], color = 'yellow', label = 'Charter')
plt.plot(list(df_treat2016.index),
         df_treat2016['avescores']['score_mean'], color='green', label='2016-17 DOI Implementers')
plt.plot(list(df_treat2017.index),
         df_treat2017['avescores']['score_mean'], color='blue', label='2017-18 DOI Implementers')
plt.plot(list(df_treat2018.index),
         df_treat2018['avescores']['score_mean'], color='orange', label='2018-19 DOI Implementers')

plt.legend()


plt.fill_between(list(df_treat2016.index), df_treat2016.lb,
                 df_treat2016.ub, color='green', alpha=.2)
plt.fill_between(list(df_treat2017.index), df_treat2017.lb,
                 df_treat2017.ub, color='blue', alpha=.2)
plt.fill_between(list(df_treat2018.index), df_treat2018.lb,
                 df_treat2018.ub, color='orange', alpha=.2)

plt.axvline(x=2016.5, color='green')
plt.axvline(x=2017.5, color='blue')
plt.axvline(x=2018.5, color='orange')


plt.ylabel('Average STAAR Scores (Std.)')
plt.title('Student Performance by District Type and DOI Implementation Year')
plt.xlabel('Test Year (Spring)', size='medium')


plt.savefig(start.table_path + 'all districts and dates.png',
            dpi=600, bbox_inches="tight")
plt.show()


# # Evidence of Parallel Trends

# In[8]:


plt.style.use('seaborn')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(list(df_treat2016[df_treat2016.index <= 2016].index), df_treat2016[df_treat2016.index <= 2016]['avescores']['score_mean'], color = 'green', label = '2016-17 DOI Implementers')
plt.plot(list(df_treat2017[df_treat2017.index <= 2017].index), df_treat2017[df_treat2017.index <= 2017]['avescores']['score_mean'], color = 'blue', label = '2017-18 DOI Implementers')
plt.plot(list(df_treat2018[df_treat2018.index <= 2018].index), df_treat2018[df_treat2018.index <= 2018]['avescores']['score_mean'], color = 'orange', label = '2018-19 DOI Implementers')

plt.legend()

plt.fill_between(list(df_treat2016[df_treat2016.index <= 2016].index), df_treat2016[df_treat2016.index <= 2016].lb, df_treat2016[df_treat2016.index <= 2016].ub, color = 'green', alpha = .2)
plt.fill_between(list(df_treat2017[df_treat2017.index <= 2017].index), df_treat2017[df_treat2017.index <= 2017].lb, df_treat2017[df_treat2017.index <= 2017].ub, color = 'blue', alpha = .2)
plt.fill_between(list(df_treat2018[df_treat2018.index <= 2018].index), df_treat2018[df_treat2018.index <= 2018].lb, df_treat2018[df_treat2018.index <= 2018].ub, color = 'orange', alpha = .2)


plt.ylabel('Average STAAR Scores (Std.)')
plt.title('Student Performance by District Type and DOI Implementation Year')
plt.xlabel('Test Year (Spring)', size = 'medium')

plt.savefig(start.table_path + 'parallel_trends_by_adoption.png', bbox_inches="tight")

plt.show()


# # Visual Impact by Subject

# In[9]:


def create_group_df(df, outcome):
    df['outcome'] = df[outcome]
    new_df = pd.DataFrame(df.groupby(['year']).agg({'outcome': ['mean', 'sem']}))
    new_df = new_df.rename(columns = {'mean': 'score_mean', 'sem': 'score_se'})
    new_df['ub'] = new_df['outcome']['score_mean'] + new_df['outcome']['score_se']
    new_df['lb'] = new_df['outcome']['score_mean'] - new_df['outcome']['score_se']
    return new_df


# In[10]:


outcome = 'elem_reading'
df_treat2016 = create_group_df(data[data.doi_year == 2016], outcome = outcome)
df_treat2017 = create_group_df(data[data.doi_year == 2017], outcome = outcome)
df_treat2018 = create_group_df(data[data.doi_year == 2018], outcome = outcome)
df_charter = create_group_df(data[data.distischarter == 'Y'], outcome = outcome)
df_treat2016


# In[11]:


title_labels = {'avescores': 'Average STAR', 'elem_math': 'Elementary Math', 'elem_reading': 'Elementary Reading',
               'middle_math': 'Middle School Math', 'middle_reading': 'Middle School Reading',
               'biology': 'Biology', 'algebra': 'Algebra', 'eng1': 'English I'}


# In[12]:


# Create cycler object. Use any styling from above you please
for outcome in ['avescores', 'elem_math', 'elem_reading', 'middle_math', 'middle_reading', 'biology', 'algebra', 'eng1']:
    df_treat2016 = create_group_df(data[data.doi_year == 2016], outcome = outcome)
    df_treat2017 = create_group_df(data[data.doi_year == 2017], outcome = outcome)
    df_treat2018 = create_group_df(data[data.doi_year == 2018], outcome = outcome)

    monochrome = (cycler('color', ['k']) * cycler('linestyle', ['-', '--', ':', '=.']))

    fig, ax = plt.subplots(1,1)
    ax.set_prop_cycle(monochrome)

    ax.plot(list(df_treat2016.index), df_treat2016['outcome']['score_mean'], label = '2016-17 DOI Implementers')
    ax.plot(list(df_treat2017.index), df_treat2017['outcome']['score_mean'],label = '2017-18 DOI Implementers')
    ax.plot(list(df_treat2018.index), df_treat2018['outcome']['score_mean'], label = '2018-19 DOI Implementers')

    ax.legend()


    ax.fill_between(list(df_treat2016.index), df_treat2016.lb, df_treat2016.ub, alpha = .2)
    ax.fill_between(list(df_treat2017.index), df_treat2017.lb, df_treat2017.ub, alpha = .2)
    ax.fill_between(list(df_treat2018.index), df_treat2018.lb, df_treat2018.ub, alpha = .2)

    ax.axvline(x = 2016.5, linestyle = '-', color = 'black')
    ax.axvline(x = 2017.5, linestyle = '--', color = 'black')
    ax.axvline(x = 2018.5, linestyle = ':', color = 'black')

    ax.set_title(title_labels[outcome])
    ax.grid(False)

    fig.savefig(table_path + 'trends_by_adoption_' + outcome + '.png', bbox_inches="tight")


# In[13]:


my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(list(df_treat2016[df_treat2016.index <= 2016].index), df_treat2016[df_treat2016.index <= 2016]['outcome']['score_mean'], label = '2016-17 DOI Implementers')
plt.plot(list(df_treat2017[df_treat2017.index <= 2017].index), df_treat2017[df_treat2017.index <= 2017]['outcome']['score_mean'], label = '2017-18 DOI Implementers')
plt.plot(list(df_treat2018[df_treat2018.index <= 2018].index), df_treat2018[df_treat2018.index <= 2018]['outcome']['score_mean'], label = '2018-19 DOI Implementers')

plt.legend()

plt.fill_between(list(df_treat2016[df_treat2016.index <= 2016].index), df_treat2016[df_treat2016.index <= 2016].lb, df_treat2016[df_treat2016.index <= 2016].ub, alpha = .2)
plt.fill_between(list(df_treat2017[df_treat2017.index <= 2017].index), df_treat2017[df_treat2017.index <= 2017].lb, df_treat2017[df_treat2017.index <= 2017].ub, alpha = .2)
plt.fill_between(list(df_treat2018[df_treat2018.index <= 2018].index), df_treat2018[df_treat2018.index <= 2018].lb, df_treat2018[df_treat2018.index <= 2018].ub, alpha = .2)


plt.ylabel('Average STAAR Scores (Std.)')
plt.title('Student Performance by District Type and DOI Implementation Year')
plt.xlabel('Test Year (Spring)', size = 'medium')

plt.savefig(table_path + 'parallel_trends_by_adoption' + outcome + '.png', bbox_inches="tight")

plt.show()


# # Demographic Trends

# In[14]:


df_control = pd.DataFrame(data[data.doi == False].groupby(['year'])['students_hisp'].mean()).reset_index()
df_treat2016 = pd.DataFrame(data[data.doi_year == 2016].groupby(['year'])['students_hisp'].mean()).reset_index()
df_treat2017 = pd.DataFrame(data[data.doi_year == 2017].groupby(['year'])['students_hisp'].mean()).reset_index()
df_treat2018 = pd.DataFrame(data[data.doi_year == 2018].groupby(['year'])['students_hisp'].mean()).reset_index()
df_treat2018


# In[15]:


plt.style.use('seaborn')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(df_control.year, df_control.students_hisp, color = 'red', label = 'TPS')
plt.plot(df_treat2016.year, df_treat2016.students_hisp, color = 'green', label = '2016-17 Implementers')
plt.plot(df_treat2017.year, df_treat2017.students_hisp, color = 'blue', label = '2017-18 Implementers')
plt.plot(df_treat2018.year, df_treat2018.students_hisp, color = 'orange', label = '2018-19 Implementers')

plt.legend()



plt.ylabel('Percent Hispanic')
plt.title('Districts of Innovation and Student Performance')
plt.xlabel('Year', size = 'medium')

#plt.savefig(table_path + 'CITS.png', bbox_inches="tight")

plt.show()


# In[16]:


df_control = pd.DataFrame(data[data.doi == False].groupby(['year'])['students_num'].mean()).reset_index()
df_treat2016 = pd.DataFrame(data[data.doi_year == 2016].groupby(['year'])['students_num'].mean()).reset_index()
df_treat2017 = pd.DataFrame(data[data.doi_year == 2017].groupby(['year'])['students_num'].mean()).reset_index()
df_treat2018 = pd.DataFrame(data[data.doi_year == 2018].groupby(['year'])['students_num'].mean()).reset_index()
df_treat2018


# In[17]:


plt.style.use('seaborn')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(df_control.year, df_control.students_num, color = 'red', label = 'TPS')
plt.plot(df_treat2016[df_treat2016.year <= 2016].year, df_treat2016[df_treat2016.year <= 2016].students_num, color = 'green', label = '2016-17 Implementers')
plt.plot(df_treat2017[df_treat2017.year <= 2017].year, df_treat2017[df_treat2017.year <= 2017].students_num, color = 'blue', label = '2017-18 Implementers')
plt.plot(df_treat2018[df_treat2018.year <= 2018].year, df_treat2018[df_treat2018.year <= 2018].students_num, color = 'orange', label = '2018-19 Implementers')

plt.legend()



plt.ylabel('Number of Students')
plt.title('Districts of Innovation and Student Performance')
plt.xlabel('Year', size = 'medium')

#plt.savefig(table_path + 'CITS.png', bbox_inches="tight")

plt.show()


# In[18]:


#  Who are 2016-17 implementers
data[(data.doi_year == 2016) & (data.year == 2018)][['distname', 'students_num']]


# # Inputs

# In[20]:


df_treat2016 = pd.DataFrame(data[data.doi_year == 2016].groupby(['year'])['stu_teach_ratio'].mean()).reset_index()
df_treat2017 = pd.DataFrame(data[data.doi_year == 2017].groupby(['year'])['stu_teach_ratio'].mean()).reset_index()
df_treat2018 = pd.DataFrame(data[data.doi_year == 2018].groupby(['year'])['stu_teach_ratio'].mean()).reset_index()

plt.style.use('seaborn')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(df_treat2016[df_treat2016.year <= 2016].year, df_treat2016[df_treat2016.year <= 2016].stu_teach_ratio, color = 'green', label = '2016-17 Implementers')
plt.plot(df_treat2017[df_treat2017.year <= 2017].year, df_treat2017[df_treat2017.year <= 2017].stu_teach_ratio, color = 'blue', label = '2017-18 Implementers')
plt.plot(df_treat2018[df_treat2018.year <= 2018].year, df_treat2018[df_treat2018.year <= 2018].stu_teach_ratio, color = 'orange', label = '2018-19 Implementers')

plt.legend()



plt.ylabel('Number of Students')
plt.title('Districts of Innovation and Student Performance')
plt.xlabel('Year', size = 'medium')

#plt.savefig(table_path + 'CITS.png', bbox_inches="tight")

plt.show()


# In[21]:


df_treat2016 = pd.DataFrame(data[data.doi_year == 2016].groupby(['year'])['certification'].mean()).reset_index()
df_treat2017 = pd.DataFrame(data[data.doi_year == 2017].groupby(['year'])['certification'].mean()).reset_index()
df_treat2018 = pd.DataFrame(data[data.doi_year == 2018].groupby(['year'])['certification'].mean()).reset_index()

plt.style.use('seaborn')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(df_treat2016[df_treat2016.year <= 2016].year, df_treat2016[df_treat2016.year <= 2016].certification, color = 'green', label = '2016-17 Implementers')
plt.plot(df_treat2017[df_treat2017.year <= 2017].year, df_treat2017[df_treat2017.year <= 2017].certification, color = 'blue', label = '2017-18 Implementers')
plt.plot(df_treat2018[df_treat2018.year <= 2018].year, df_treat2018[df_treat2018.year <= 2018].certification, color = 'orange', label = '2018-19 Implementers')

plt.legend()



plt.ylabel('Number of Students')
plt.title('Districts of Innovation and Student Performance')
plt.xlabel('Year', size = 'medium')

#plt.savefig(table_path + 'CITS.png', bbox_inches="tight")

plt.show()


# In[38]:


df_treat2016 = pd.DataFrame(data[data.doi_year == 2016].groupby(['year'])['class_size_5'].mean()).reset_index()
df_treat2017 = pd.DataFrame(data[data.doi_year == 2017].groupby(['year'])['class_size_5'].mean()).reset_index()
df_treat2018 = pd.DataFrame(data[data.doi_year == 2018].groupby(['year'])['class_size_5'].mean()).reset_index()

plt.style.use('seaborn')
my_dpi=96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(df_treat2016[df_treat2016.year <= 2016].year, df_treat2016[df_treat2016.year <= 2016].class_size_5, color = 'green', label = '2016-17 Implementers')
plt.plot(df_treat2017[df_treat2017.year <= 2017].year, df_treat2017[df_treat2017.year <= 2017].class_size_5, color = 'blue', label = '2017-18 Implementers')
plt.plot(df_treat2018[df_treat2018.year <= 2018].year, df_treat2018[df_treat2018.year <= 2018].class_size_5, color = 'orange', label = '2018-19 Implementers')

plt.legend()



plt.ylabel('Number of Students')
plt.title('Districts of Innovation and Student Performance')
plt.xlabel('Year', size = 'medium')

#plt.savefig(table_path + 'CITS.png', bbox_inches="tight")

plt.show()


# In[24]:


list(data.columns)


# In[36]:


data['class_size_5'] = pd.to_numeric(data['class_size_5'],errors='coerce')
data.class_size_5.mean()


# In[ ]:

