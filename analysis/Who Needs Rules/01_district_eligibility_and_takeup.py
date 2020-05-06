# %%
import os
import sys

import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl import load_workbook
from patsy import dmatrices

sys.path.append("../")
from library import start


plt.style.use('grayscale')


# %%

data = pd.read_csv(os.path.join(start.data_path, 'clean',
                                'master_data_district.csv'), sep=",",
                   low_memory=False)
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
print('Number of ineligible TPSDs in 2019:')
print(data19[data19.eligible == 0].district.nunique())
print('What % of traditional public school district were eligible in 2015?')
print(data15.eligible.mean())
print('And in 2017-18?')
print(data18.eligible.mean())
print('And in 2018-19?')
print(data19.eligible.mean())

print('How many tradtional public districts are DOIs as of March 2019?')
print(data.loc[data.doi].district.nunique())
print('Only', data19.loc[(~data19.doi) & (data19.eligible)
                         ].district.nunique(), 'districts have opted out.')
print('What percent of districts are DOIs as of March 2019?')
print(data.loc[data.doi].district.nunique() /
      data[data.distischarter == 0].district.nunique())


# %%


district_df = pd.DataFrame(data.groupby(
    ['district']).agg({'doi_year': 'mean'}))
district_counts = pd.DataFrame(district_df.doi_year.value_counts(sort=False))
print(district_counts)
district_counts = district_counts.sort_index()
print('Cumulative count of DOIs in each year:')
print(district_counts.doi_year.cumsum())

my_dpi = 96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)

# Pre
plt.plot(district_counts.index,
         district_counts.doi_year.cumsum(), color='black')
plt.xticks([int(i) for i in list(district_counts.index)])

plt.ylabel('Number of Districts')
plt.title('Texas District of Innovation Adoption Over Time')
plt.xlabel('Test Year (Spring)', size='medium')
plt.grid(True, alpha=.6)


plt.ylim(0, 1022)
txt = "Notes: Statistics are as of March 2019. "
"There are ten Districts of Innovation (with missing Innovation Plans) \n "
"that are not included in the figure. "
"As of 2019, there were 1022 traditional public school districts in Texas."
plt.figtext(.5, -.01, txt, wrap=True, horizontalalignment='center', fontsize=8)

plt.savefig(start.table_path + 'takeup.png', dpi=600, bbox_inches="tight")
plt.show()

