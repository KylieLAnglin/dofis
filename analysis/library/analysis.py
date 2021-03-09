import numpy as np


import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy.stats import ttest_ind


def coef_with_stars(coef: float, pvalue: float, n_tests: int = 1, digits: int = 2):
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

    coef = round(coef, digits)
    if pvalue > (0.05 / n_tests):
        coef = str(coef)
    if pvalue <= (0.05 / n_tests):
        coef = str(coef) + "*"
    if pvalue <= (0.01 / n_tests):
        coef = coef + "*"
    if pvalue <= (0.001 / n_tests):
        coef = coef + "*"
    return coef


def format_se(se, digits: int = 2):
    """round and format standard error

    rounded to two decimals. surround by parens.

    Args:
        se ([type]): [description]

    Returns:
        [type]: [description]
    """

    se_formatted = "(" + str(round(se, digits)) + ")"
    return se_formatted


def many_y_one_x(data, y_list, y_labels, x):
    regs = []
    cons = []
    coef = []
    se = []
    pvalue = []

    for y in y_list:
        formula = y + " ~ + 1 + " + x
        print(formula)
        df = data.replace(np.inf, np.nan).replace(-np.inf, np.nan).dropna(subset=[y])
        result = smf.ols(formula=formula, data=data).fit()
        print(result.summary())
        cons.append(result.params["Intercept"].round(2))
        if str(data[x].dtypes) == "bool":
            var = x + "[T.True]"
        else:
            var = x
        coef.append(result.params[var].round(2))
        se.append(result.bse[var].round(2))
        pvalue.append(result.pvalues[var].round(2))
        regs.append(y_labels[y])

    df = pd.DataFrame(
        {
            "Characteristic": regs,
            "Control": cons,
            "Difference": coef,
            "Std. Error": se,
            "P-value": pvalue,
        }
    )
    return df


def many_x_one_y(data, y, x_list, x_labels):
    regs = []
    cons = []
    coef = []
    se = []
    pvalue = []

    for x in x_list:
        formula = y + " ~ " + x
        result = smf.ols(formula=formula, data=data).fit()
        cons.append(result.params["Intercept"].round(2))
        var = x
        coef.append(result.params[var].round(2))
        se.append(result.bse[var].round(2))
        pvalue.append(result.pvalues[var].round(2))
        regs.append(x_labels[x])

    df = pd.DataFrame(
        {
            "Characteristic": regs,
            "Control": cons,
            "Difference": coef,
            "Std. Error": se,
            "P-value": pvalue,
        }
    )
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

        ttest = ttest_ind(nonexempt[var], exempt[var], nan_policy="omit")
        pvalue = ttest[1]
        if pvalue > 0.1:
            stars = ""
        if pvalue <= 0.1:
            stars = "+"
        if pvalue <= 0.05:
            stars = "*"
        if pvalue <= 0.01:
            stars = "**"
        if pvalue <= 0.001:
            stars = "***"
        pvalues_col.append(stars)
        # pvalues_col.append(ttest[1].round(2))

    data = pd.DataFrame(columns=["variable", "nonexempt", "exempt", "pvalue"])
    data["variable"] = variables
    data["nonexempt"] = nonexempt_col
    data["exempt"] = exempt_col
    data["pvalue"] = pvalues_col

    return data


def create_interactions(variable: str, data: pd.DataFrame):
    data["treatpost_" + variable] = data["treatpost"] * data[variable]
    data["yearpost_" + variable] = data["yearpost"] * data[variable]
    data["yearpre_" + variable] = data["yearpre"] * data[variable]

    for preyr in [5, 4, 3, 2]:
        data[variable + "_pre" + str(preyr)] = data[variable] * data["pre" + str(preyr)]
    for postyr in [1, 2, 3]:
        data[variable + "_post" + str(postyr)] = (
            data[variable] * data["post" + str(postyr)]
        )
    return data


def create_gdid_model_w_interactions(variable: str):
    # no need for variable effect alone because this is captured by
    # entity effects
    gdid_model = "score_std ~ + 1 + treatpost + "
    gdid_model = gdid_model + "treatpost_" + variable + " + "
    gdid_model = gdid_model + "C(test_by_year) + "
    gdid_model = gdid_model + "EntityEffects"
    print(gdid_model)
    return gdid_model


def create_linear_model_w_interactions(variable: str):
    linear_gdid_model = "score_std ~ + 1 + treatpost + yearpost + yearpre + "
    linear_gdid_model = linear_gdid_model + "treatpost_" + variable + " + "
    linear_gdid_model = linear_gdid_model + "yearpre_" + variable + " + "
    linear_gdid_model = linear_gdid_model + "yearpost_" + variable + " + "
    linear_gdid_model = linear_gdid_model + " + C(test_by_year) + "
    linear_gdid_model = linear_gdid_model + "EntityEffects"

    return linear_gdid_model


def create_event_model_w_interactions(variable: str):
    event_study_model = (
        "score_std ~ + 1 + pre5 + pre4 + pre3 + pre2 + " "post1 + post2 + post3"
    )
    for preyr in ["_pre5", "_pre4", "_pre3", "_pre2"]:
        event_study_model = event_study_model + " + " + variable + preyr
    for postyr in ["_post1", "_post2", "_post3"]:
        event_study_model = event_study_model + " + " + variable + postyr
    event_study_model = event_study_model + " + C(test_by_year) + EntityEffects"
    print(event_study_model)

    return event_study_model


def double_covariate_selection(
    outcome1: str,
    outcome2: str,
    data: pd.DataFrame,
    covariates: list,
    alpha: float = 0.01,
):
    data = data.copy()
    data = data[[outcome1, outcome2] + covariates]
    data = data.dropna()
    """Performs the double selection procedure suggested by Belloni, Chernozhukov, Fernández, and Hansen

    Args:
        outcome1 (str): Column containing treatment indicator variable in data
        outcome2 (str): Column containing outcome in data
        data (pd.DataFrame): Data with treatment, outcome, and covariates
        covariates (list): Potential covariates in data to select from
        alpha (float): alpha for lasso regression

    Returns:
        [type]: [description]
    """
    variables = []
    X = data[covariates]

    mod = sm.OLS(data[outcome1], X)
    res = mod.fit_regularized(alpha=alpha, L1_wt=1, refit=True)

    for variable, coefficient in zip(list(X.columns), list(res.params)):
        if coefficient > 0:
            variables.append(variable)

    mod = sm.OLS(data[outcome1], X)
    res = mod.fit_regularized(alpha=alpha, L1_wt=1, refit=True)

    for variable, coefficient in zip(list(X.columns), list(res.params)):
        if (variable not in variables) & (coefficient > 0):
            variables.append(variable)

    return variables


def simple_did_df(
    group_var: str,
    group: int,
    time_var: str,
    time: int,
    df: pd.DataFrame,
):
    """Subsets a dataframe so that it only contains two groups
    and two time periods,

    Args:
        group_var (str): column containing group variable
        group (int): value in group column of dataframe to be treated
        time_var (str): column containing time variable
        time (int): value in time column of dataframe to be post
        df (pd.DataFrame): dataframe containing group and time columns

    Returns:
        pd.DataFrame: Untreated rows during one pre period, treat and untreated in one post
        new treatm, post, and treat_post columns
    """
    if time < group:  # if pre-treatment year, limit to year and year - 1
        did_df = df[(df[time_var] == time) | (df[time_var] == time - 1)]

    elif (
        time >= group
    ):  # if post-treatment year, limit to year and year before group first implemented
        did_df = df[
            (df[time_var] == time) | (df[time_var] == group - 1)
        ]  # limit to two years

    did_df = did_df[
        (did_df[group_var] == group)
        | (did_df[group_var] > time)
        | (did_df[group_var] == 0)
    ]  # limit to two groups

    did_df["treat"] = np.where(did_df[group_var] == group, 1, 0)
    did_df["post"] = np.where(did_df[time_var] == time, 1, 0)
    did_df["treat_post"] = did_df.treat * did_df.post

    return did_df


def did(
    outcome: str,
    group_var: str,
    group: int,
    time_var: str,
    time: int,
    cluster_var: str,
    df: pd.DataFrame,
):
    """Estimate simple two-group two-time Diff-in-Diff

    Args:
        outcome (str): outcome column
        group_var (str): implementation group column with time of implementation where 0 indicates never treated
        group (int): implementation group of interest
        time_var (str): time column (should be in same units as group var)
        time (int): time of interest (pre-time is one less this value)
        cluster_var (str): cluster id column
        df (pd.DataFrame): dataset containing outcome, group_var, time_var, and cluster_var

    Returns:
        [type]: [description]
    """
    did_df = simple_did_df(
        group_var=group_var, group=group, time_var=time_var, time=time, df=df
    )
    mod = smf.ols(outcome + " ~ 1 + treat + post + treat_post", did_df)
    res = mod.fit(cov_type="cluster", cov_kwds={"groups": did_df[cluster_var]})
    print(res.summary())
    return res


def dids(
    outcome: str, group_var: str, time_var: str, cluster_var: str, df: pd.DataFrame
):

    groups = np.sort(df[df.group != 0][group_var].unique())
    times = np.sort(df[df[time_var] > df[time_var].min()][time_var].unique())
    group_time_combos = [
        {"group": group, "time": time} for time in times for group in groups
    ]

    group_results = {int(group): {} for group in groups}

    for combo in group_time_combos:
        group = combo["group"]
        time = combo["time"]

        did_result = did(
            outcome=outcome,
            group_var=group_var,
            group=group,
            time_var=time_var,
            time=time,
            cluster_var=cluster_var,
            df=df,
        )

        group_results[group][time] = did_result

    return group_results