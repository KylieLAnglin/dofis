# %%

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS

from dofis.analysis.library import analysis
from dofis.analysis.library import regulations
from dofis.analysis.library import start

# %% School Data
data_school = pd.read_csv(os.path.join(start.data_path, 'clean',
                                       'master_data_school.csv'), sep=",",
                          low_memory=False)
data_school = data_school[data_school.doi]
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

# %% Effect Certificaiton


df = pd.read_csv(os.path.join(start.data_path, 'clean',
                                       'gdid_school.csv'), sep=",",
                          low_memory=False)
df = df[~df.certified.isnull()]
df = df[df.post3 ==0]

# convert year to datetime
df = df.reset_index()
df['year'] = pd.to_datetime(df['year'], format='%Y')
# add column year to index
df = df.set_index(['year', 'campus'])
# swap indexes
df.index = df.index.swaplevel(0, 1)


event_study_model = 'certified ~ + 1 + pre5 + pre4 + pre3 + pre2 + ' \
    'post1 + post2 + EntityEffects + TimeEffects'

mod = PanelOLS.from_formula(event_study_model, data = df)
res = mod.fit(cov_type='clustered', clusters=df.district)
nonparametric = []
nonparametric_se = []
for coef in ['pre5', 'pre4', 'pre3', 'pre2',
             'pre1', 'post1', 'post2']:
    nonpar = 0
    nonpar_se = 0
    if coef != 'pre1':
        nonpar = res.params[coef]
        nonpar_se = res.std_errors[coef]
    nonparametric.append(nonpar)
    nonparametric_se.append(nonpar_se)
coef_df = pd.DataFrame({'coef': nonparametric,
                        'err': nonparametric_se,
                        'year': [-5, -4, -3, -2, -1, 1, 2]
                        })
coef_df['lb'] = coef_df.coef - (1.96*coef_df.err)
coef_df['ub'] = coef_df.coef + (1.96*coef_df.err)
coef_df['errsig'] = coef_df.err * 1.96

fig, ax = plt.subplots(figsize=(8, 5))

coef_df.plot(x='year', y='coef', kind='bar',
             ax=ax, color='none',
             yerr='errsig', legend=False)
ax.set_ylabel('')
ax.set_xlabel('')
ax.scatter(x=pd.np.arange(coef_df.shape[0]),
           marker='s', s=120,
           y=coef_df['coef'], color='black')
ax.axhline(y=0, linestyle='--', color='black', linewidth=4)
ax.xaxis.set_ticks_position('none')
_ = ax.set_xticklabels(['Pre5', 'Pre4', 'Pre3', 'Pre2', 'Pre1',
                        'Post1', 'Post2'],
                       rotation=0)
# ax.set_title('Impact on Student Achievement - Event Study Coefficients',
#  fontsize = 16)

fig.savefig(start.table_path + 'certification_event_study' + '.png',
            bbox_inches="tight")


# %%
