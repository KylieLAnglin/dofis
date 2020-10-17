import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import ttest_ind
import numpy as np


def coef_with_stars(coef: float, pvalue: float, n_tests: int = 1):
    """Creates rounded formatted values for tables w/stars.

    Numbers are rounded to two decimals, with three stars \
    for p-value <= .001, two for <= .01, one for <=.05. If \
    bonferroni adjustment is appropriate, specify number of tests

    coef: numeric
        Statstic to put in table
    pvalue: numeric
        pvalue of statistic
    n_tests: numeric (optional)
        number of tests for bonferroni adjustment

    returns string
        formatted coefficient

    """
    coef = float(coef)
    
    coef = round(coef, 2)
    if pvalue > (.05/n_tests):
        coef = str(coef)
    if pvalue <= (.05/n_tests):
        coef = str(coef) + '*'
    if pvalue <= (.01/n_tests):
        coef = coef + '*'
    if pvalue <= (.001/n_tests):
        coef = coef + '*'
    return(coef)



def bonferroni(n_tests, coef, pvalue):
    """creates rounded formatted strings with stars adjusted /
    for multiple hypothesis testing

    Args:
        n_tests (numeric): number of hypothesis tests
        coef (numeric): statistic
        pvalue ([numeric]): p-value
    """
    coef = round(coef, 2)
    if pvalue > (.05/n_tests):
        coef = str(coef)
    if pvalue <= (.05/n_tests):
        coef = str(coef) + '*'
    if pvalue <= (.01/n_tests):
        coef = coef + '*'
    if pvalue <= (.001/n_tests):
        coef = coef + '*'
    return(coef)


def format_se(se):
    """round and format standard error

    rounded to two decimals. surround by parens.

    Args:
        se ([type]): [description]

    Returns:
        [type]: [description]
    """

    if se < .005:
        se = '(0.00)'
    else:
        se = '(' + str(round(se, 2)) + ')'
    return se


def create_count_proportion_df(data, list_of_regs, dict_of_reg_labels):
    n_col = []
    p_urban = []
    p_suburb = []
    p_town = []
    p_rural = []
    reg_labels = []
    f_p = []

    for reg in list_of_regs:
        n_col.append((len(data[data[reg] == 1])))
        p_urban.append(data[data.type_urban == 1][reg].mean().round(2))
        p_suburb.append(data[data.type_suburban == 1][reg].mean().round(2))
        p_town.append(data[data.type_town == 1][reg].mean().round(2))
        p_rural.append(data[data.type_rural == 1][reg].mean().round(2))
        reg_labels.append(dict_of_reg_labels[reg])
        formula = reg + '~ type_urban + type_suburban + type_town + type_rural - 1'
        df = data.dropna(
            subset=['type_urban', 'type_suburban', 'type_town', 'type_rural', reg])
        results = smf.ols(formula, data=df).fit()
        f_p.append(results.f_pvalue.round(2))

    df = pd.DataFrame(
        {'Regulation': reg_labels,
         'Count': n_col,
         'Percent Urban': p_urban,
         'Percent Suburban': p_suburb,
         'Percent Town': p_town,
         'Percent Rural': p_rural,
         'F-test p-value': f_p
         })

    return df


def many_y_one_x(data, y_list, y_labels, x):
    regs = []
    cons = []
    coef = []
    se = []
    pvalue = []

    for y in y_list:
        formula = y + ' ~ + 1 + ' + x
        print(formula)
        df = data.replace(np.inf, np.nan).replace(-np.inf,
                                                  np.nan).dropna(subset=[y])
        result = smf.ols(formula=formula, data=data).fit()
        print(result.summary())
        cons.append(result.params["Intercept"].round(2))
        if str(data[x].dtypes) == 'bool':
            var = x + '[T.True]'
        else:
            var = x
        coef.append(result.params[var].round(2))
        se.append(result.bse[var].round(2))
        pvalue.append(result.pvalues[var].round(2))
        regs.append(y_labels[y])

    df = pd.DataFrame(
        {'Characteristic': regs,
         'Control': cons,
         'Difference': coef,
         'Std. Error': se,
         'P-value': pvalue,
         })
    return df


def many_x_one_y(data, y,  x_list, x_labels):
    regs = []
    cons = []
    coef = []
    se = []
    pvalue = []

    for x in x_list:
        formula = y + ' ~ ' + x
        result = smf.ols(formula=formula, data=data).fit()
        cons.append(result.params["Intercept"].round(2))
        var = x
        coef.append(result.params[var].round(2))
        se.append(result.bse[var].round(2))
        pvalue.append(result.pvalues[var].round(2))
        regs.append(x_labels[x])

    df = pd.DataFrame(
        {'Characteristic': regs,
         'Control': cons,
         'Difference': coef,
         'Std. Error': se,
         'P-value': pvalue,
         })
    return df


def two_means_by_exemptions(df, exemption, var_list):
    nonexempt = df[df[exemption] == False]
    exempt = df[df[exemption] == True]

    variables = var_list
    nonexempt_col = []
    exempt_col = []
    pvalues_col = []
    for var in variables:

        nonexempt_col.append(nonexempt[var].mean().round(2))
        exempt_col.append(exempt[var].mean().round(2))

        ttest = ttest_ind(nonexempt[var], exempt[var], nan_policy='omit')
        pvalue = ttest[1]
        if pvalue > .1:
            stars = ''
        if pvalue <= .1:
            stars = '+'
        if pvalue <= .05:
            stars = '*'
        if pvalue <= .01:
            stars = '**'
        if pvalue <= .001:
            stars = '***'
        pvalues_col.append(stars)
        # pvalues_col.append(ttest[1].round(2))

    data = pd.DataFrame(columns=['variable', 'nonexempt', 'exempt', 'pvalue'])
    data['variable'] = variables
    data['nonexempt'] = nonexempt_col
    data['exempt'] = exempt_col
    data['pvalue'] = pvalues_col

    return data


def create_interactions(variable: str, data: pd.DataFrame):
    data['treatpost_' + variable] = data['treatpost'] * data[variable]
    data['yearpost_' + variable] = data['yearpost'] * data[variable]
    data['yearpre_' + variable] = data['yearpre'] * data[variable]

    for preyr in [5, 4, 3, 2]:
        data[variable + '_pre' + str(preyr)] = data[variable] * data['pre' + str(preyr)]
    for postyr in [1, 2, 3]:
        data[variable + '_post' + str(postyr)] = data[variable] * data['post' + str(postyr)]
    return data

def create_gdid_model_w_interactions(variable: str):
    # no need for variable effect alone because this is captured by
    # entity effects
    gdid_model = 'score_std ~ + 1 + treatpost + '
    gdid_model = gdid_model + 'treatpost_' + variable + ' + '
    gdid_model = gdid_model + 'C(test_by_year) + '
    gdid_model = gdid_model + 'EntityEffects'
    print(gdid_model)
    return gdid_model


def create_linear_model_w_interactions(variable: str):
    linear_gdid_model = 'score_std ~ + 1 + treatpost + yearpost + yearpre + '
    linear_gdid_model = linear_gdid_model + 'treatpost_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + 'yearpre_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + 'yearpost_' + variable + ' + '
    linear_gdid_model = linear_gdid_model + ' + C(test_by_year) + '
    linear_gdid_model = linear_gdid_model + 'EntityEffects'

    return linear_gdid_model


def create_event_model_w_interactions(variable: str):
    event_study_model = 'score_std ~ + 1 + pre5 + pre4 + pre3 + pre2 + ' \
        'post1 + post2 + post3'
    for preyr in ["_pre5", "_pre4", "_pre3", "_pre2"]:
        event_study_model = event_study_model + ' + ' + variable + preyr
    for postyr in ["_post1", "_post2", "_post3"]:
        event_study_model = event_study_model + ' + ' + variable + postyr
    event_study_model = event_study_model + ' + C(test_by_year) + EntityEffects'
    print(event_study_model)

    return event_study_model