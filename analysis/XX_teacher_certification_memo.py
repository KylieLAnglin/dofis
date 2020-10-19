# %%

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from dofis.analysis.library import analysis
from dofis.analysis.library import regulations
from dofis.analysis.library import start

# %% School Data
data_school = pd.read_csv(os.path.join(start.data_path, 'clean',
                                       'master_data_school.csv'), sep=",",
                          low_memory=False)
# %%

school_df = pd.DataFrame(data_school.groupby(
    ['campus']).agg({'doi_year': 'mean'}))
school_counts = pd.DataFrame(school_df.doi_year.value_counts(sort=False))
school_counts = school_counts.sort_index()

exempt_cert = data_school[data_school.exempt_certification == 1]
cert_df = pd.DataFrame(exempt_cert).groupby(
    ['campus']).agg({'doi_year': 'mean'})

cert_counts = pd.DataFrame(cert_df.doi_year.value_counts(sort=False))
cert_counts = cert_counts.sort_index()


# %%

my_dpi = 96
plt.figure(figsize=(480/my_dpi, 480/my_dpi), dpi=my_dpi)


plt.plot(school_counts.index,
         school_counts.doi_year.cumsum(), color='black')


plt.plot(cert_counts.index,
         cert_counts.doi_year.cumsum(), color='gray')


plt.xticks([int(i) for i in list(school_counts.index)])

plt.ylabel('Number of Schools')
plt.title('Texas District of Innovation Adoption Over Time')
plt.xlabel('Test Year (Spring)', size='medium')
plt.grid(True, alpha=.6)


txt = "Notes: Statistics are as of June 2019. "
plt.figtext(.5, -.01, txt, wrap=True,
            horizontalalignment='center', fontsize=8)

plt.show()

# %%
