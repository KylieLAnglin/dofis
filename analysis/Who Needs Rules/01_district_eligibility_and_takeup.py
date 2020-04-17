# %%
import sys
sys.path.append("../")
import os
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from patsy import dmatrices
from openpyxl import load_workbook
from library import start

import matplotlib
plt.style.use('grayscale')


# %%

data = pd.read_csv(os.path.join(start.data_path, 'clean', 'master_data_district.csv'), 
sep=",", low_memory= False)
data15 = data[data.year == 2015]
data18 = data[data['year'] == 2018]
data19 = data[data['year'] == 2019]

# Ignore charters
data15 = data15[data15.distischarter == 0]
data18 = data18[data18.distischarter == 0]
data19 = data19[data19.distischarter == 0]


# %%
print('Number of traditional public school districts in Texas in 2019:')
print(data19.district.nunique())
print('What percent of traditional public school district were eligible in 2015?')
print(data15.eligible.mean())
print('And in 2017-18?')
print(data18.eligible.mean())
print('And in 2018-19?')
print(data19.eligible.mean())

print('How many tradtional public districts are DOIs as of March 2019?')
print(data[data.doi == True].district.nunique())
print('Only', data18[(data18.doi == False) & (data18.eligible == True)].district.nunique(), 'districts have opted out.')
print('What percent of districts are DOIs as of March 2019?')
print(data[data.doi == True].district.nunique()/data[data.distischarter == 0].district.nunique())


# %%


district_df = pd.DataFrame(data.groupby(['district']).agg({'doi_year': 'mean'}))
district_counts = pd.DataFrame(district_df.doi_year.value_counts(sort = False))
district_counts = district_counts.sort_index()
print('Cumulative count of DOIs in each year:')
print(district_counts.doi_year.cumsum())

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

plt.savefig(start.table_path + 'takeup.png', dpi = 600, bbox_inches="tight")
plt.show()

