
# %%


import os
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS
from openpyxl import load_workbook
from patsy import dmatrices

sys.path.append("../")
from library import start, analysis

# %%

data_path = start.data_path
table_path = start.table_path
data = pd.read_csv(os.path.join(data_path, 'clean', 'gdid_subject.csv'),
                   sep=",", low_memory=False)
data = data[data.doi]
print(data[(data.doi)].district.nunique())
print(data.doi_year.value_counts())
data.sample(5)

df = data.reset_index()
df['year'] = pd.to_datetime(df['year'], format='%Y')
# add column year to index
df = data.set_index(['year', 'campus'])
# swap indexes
df.index = df.index.swaplevel(0, 1)
df[['district', 'doi_year', 'treatpost']].sample(5)


# %% Generate interactions

def create_interactions(variable: str, data: pd.DataFrame):
    data[variable] = data[variable] * data['treatpost']
    data['treatpost_' + variable] = data['treatpost'] * data[variable]
    data['yearpost_' + variable] = data['yearpost'] * data[variable]
    data['yearpre_' + variable] = data['yearpre'] * data[variable]
    
    for preyr in [5, 4, 3, 2]:
        data[variable + '_pre' + str(preyr)] = data[variable] * data['pre' + str(preyr)]
    for postyr in [1, 2, 3]:
         data[variable + '_post' + str(postyr)] = data[variable] * data['post' + str(preyr)]
    return data


def create_linear_model_w_interactions(variable: str):
    linear_gdid_model = 'score_std ~ + 1 + treatpost + yearpost + yearpre + '
    linear_gdid_model = linear_gdid_model + 'treatpost_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + 'yearpost_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + 'yearpre_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + ' + C(test_by_year) + '
    linear_gdid_model = linear_gdid_model + 'EntityEffects'

    return linear_gdid_model

def create_linear_model_w_interactions(variable: str):
    linear_gdid_model = 'score_std ~ + 1 + treatpost + yearpost + '
    linear_gdid_model = linear_gdid_model + 'treatpost_' + variable + ' + yearpre + '
    linear_gdid_model = linear_gdid_model + 'yearpost_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + ' + C(test_by_year) + '
    linear_gdid_model = linear_gdid_model + 'EntityEffects'

    return linear_gdid_model

def create_gdid_model_w_interactions(variable: str):
    gdid_model = 'score_std ~ + 1 + treatpost + '
    gdid_model = gdid_model + 'treatpost_' + variable + ' + '
    gdid_model = gdid_model + 'C(test_by_year) + '
    gdid_model = gdid_model + 'EntityEffects'

    return gdid_model



def create_event_model_w_interactions(variable: str):
    event_study_model = 'score_std ~ + 1 + pre5 + pre4 + pre3 + pre2 + ' \
        'post1 + post2 + post3'
    for preyr in ["_pre5", "_pre4", "_pre3", "_pre2"]:
        event_study_model = event_study_model + ' + ' + variable + preyr 
    for postyr in ["_post1", "_post2", "_post3"]:
        event_study_model = event_study_model +  ' + ' + variable + postyr
    print(event_study_model)

    return event_study_model

create_event_model_w_interactions('exempt_minutes')

df = create_interactions('exempt_minutes', df)

mod = PanelOLS.from_formula(create_event_model_w_interactions('exempt_minutes'),
                            df[df.math == 1])
res = mod.fit(cov_type='clustered', clusters=df[df.math == 1].district)
print(res)

# %%


linear_gdid_model = 'score_std ~ + 1 + treatpost + yearpost + ' \
    'yearpre  + C(test_by_year) + EntityEffects'
event_study_model = 'score_std ~ + 1 + pre5 + pre4 + pre3 + pre2 + ' \
    'post1 + post2 + post3  + C(test_by_year) + EntityEffects'

mod = PanelOLS.from_formula(event_study_model,
                            df[(df.math == 1) & (df.exempt_certification == 1)])
res = mod.fit(cov_type='clustered', clusters=df[(df.math == 1) & (df.exempt_certification == 1)].district)
print(res)

mod = PanelOLS.from_formula(event_study_model,
                            df[(df.math == 1) & (df.exempt_certification == 0)])
res = mod.fit(cov_type='clustered', clusters=df[(df.math == 1) & (df.exempt_certification == 0)].district)
print(res)

# Linear GDID
mod = PanelOLS.from_formula(linear_gdid_model, data)
res = mod.fit(cov_type='clustered', clusters=data.district)
print(res)

def results_table(data, file_name):
    file = start.table_path + file_name
    wb = load_workbook(file)
    ws = wb.active

    # GDID
    mod = PanelOLS.from_formula(gdid_model, data)
    res = mod.fit(cov_type='clustered', clusters=data.district)
    # res = mod.fit(cov_type='clustered', cluster_entity = True,
    # cluster_time = True)
    print(res)
    ws.cell(row=3, column=2).value = analysis.coef_with_stars(
        res.params['treatpost[T.True]'], res.pvalues['treatpost[T.True]'])
    ws.cell(row=4, column=2).value = analysis.format_se(
        res.std_errors['treatpost[T.True]'])

    # Linear GDID
    mod = PanelOLS.from_formula(linear_gdid_model, data)
    res = mod.fit(cov_type='clustered', clusters=data.district)
    print(res)
    ws.cell(row=6, column=2).value = analysis.coef_with_stars(
        res.params['treatpost[T.True]'], res.pvalues['treatpost[T.True]'])
    ws.cell(row=7, column=2).value = analysis.format_se(
        res.std_errors['treatpost[T.True]'])
    ws.cell(row=8, column=2).value = analysis.coef_with_stars(
        res.params['yearpost'], res.pvalues['yearpost'])
    ws.cell(row=9, column=2).value = analysis.format_se(
        res.std_errors['yearpost'])
    ws.cell(row=10, column=2).value = analysis.coef_with_stars(
        res.params['yearpre'], res.pvalues['yearpre'])
    ws.cell(row=11, column=2).value = analysis.format_se(
        res.std_errors['yearpre'])

    # Event Study
    mod = PanelOLS.from_formula(event_study_model, data)
    res = mod.fit(cov_type='clustered', clusters=data.district)
    print(res)
    row = 3
    for coef in ['post3', 'post2', 'post1', 'pre2', 'pre3', 'pre4', 'pre5']:
        ws.cell(row=row, column=4).value = analysis.coef_with_stars(
            res.params[coef], res.pvalues[coef])
        row = row + 1
        ws.cell(row=row, column=4).value = analysis.format_se(
            res.std_errors[coef])
        row = row + 1

    wb.save(file)
