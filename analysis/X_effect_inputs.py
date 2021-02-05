# %%
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl import load_workbook


from dofis.analysis.library import start
from dofis.analysis.library import characteristics
from dofis.analysis.library import analysis


COLUMNS = (
    ["year", "doi_year", "campus", "campname", "district", "distname"]
    + characteristics.POTENTIAL_COVARIATES
    + characteristics.INPUTS
    + [
        "exempt_minutes",
        "exempt_certification",
        "exempt_classsize",
        "exempt_servicedays",
    ]
)

# %%
data_school = pd.read_csv(
    os.path.join(start.data_path, "clean", "master_data_school.csv"),
    sep=",",
    low_memory=False,
)
data_school = data_school[data_school.doi]
data_school = data_school[COLUMNS]
data_school["const"] = 1

data_school = data_school.dropna(subset=characteristics.POTENTIAL_COVARIATES)
data_school = data_school.set_index("campus")

# %%
pre_data = data_school[data_school.year == 2016][characteristics.POTENTIAL_COVARIATES]
pre_data = pre_data.add_prefix("pre_")

data_school = data_school.merge(pre_data, how="left", left_index=True, right_index=True)
data_school = data_school.dropna(subset=list(data_school.filter(like="pre_").columns))


# %%
import statsmodels.api as sm


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


# %%

matching_variables = double_covariate_selection(
    "exempt_certification",
    "teachers_uncertified",
    data_school,
    list(data_school.filter(like="pre_").columns),
    alpha=0.005,
)
matching_variables


# %%
OUTCOME = "teachers_uncertified"
YEAR = 2019
TREATMENT = "exempt_certification"
COVARIATES = list(data_school.filter(like="pre_").columns)
COL = 4

model = OUTCOME + " ~ 1 + " + TREATMENT + " + "
for var in COVARIATES:
    model = model + " + " + var
model

df = data_school[data_school.year == YEAR]
df = df[df.doi_year <= YEAR]
mod = smf.ols(formula=model, data=df)
res = mod.fit(cov_type="cluster", cov_kwds={"groups": df["district"]})
print(res.summary())

file = start.table_path + "effect_uncertified_teachers.xlsx"
wb = load_workbook(file)
ws = wb.active

# Estimates
ws.cell(row=4, column=COL).value = analysis.coef_with_stars(
    res.params[TREATMENT], res.pvalues[TREATMENT], digits=3
)
ws.cell(row=5, column=COL).value = analysis.format_se(res.bse[TREATMENT])

# Sample sizes
ws.cell(row=9, column=COL).value = len(
    data_school[
        (data_school.year == YEAR)
        & (data_school.doi_year <= YEAR)
        & (data_school[TREATMENT] == 1)
    ]
)
ws.cell(row=10, column=COL).value = data_school[
    (data_school.year == YEAR)
    & (data_school.doi_year <= YEAR)
    & (data_school[TREATMENT] == 1)
].district.nunique()
ws.cell(row=11, column=COL).value = len(
    data_school[
        (data_school.year == YEAR)
        & (data_school.doi_year <= YEAR)
        & (data_school[TREATMENT] == 0)
    ]
)
ws.cell(row=12, column=COL).value = data_school[
    (data_school.year == YEAR)
    & (data_school.doi_year <= YEAR)
    & (data_school[TREATMENT] == 0)
].district.nunique()

wb.save(file)


# %%


def effect_input(outcome: str, year: str, treatment: str, data: pd.DataFrame, col: int):
    mod = smf.ols(formula=model, data=df)
    res = mod.fit(cov_type="cluster", cov_kwds={"groups": df["district"]})
    print(res.summary())

    file = start.table_path + "effect_uncertified_teachers.xlsx"
    wb = load_workbook(file)
    ws = wb.active

    # Estimates
    ws.cell(row=4, column=COL).value = analysis.coef_with_stars(
        res.params[TREATMENT], res.pvalues[TREATMENT], digits=3
    )
    ws.cell(row=5, column=COL).value = analysis.format_se(res.bse[TREATMENT])

    # Sample sizes
    ws.cell(row=9, column=COL).value = len(data_school[data_school[TREATMENT] == 1])
    ws.cell(row=10, column=COL).value = data_school[
        data_school[TREATMENT] == 1
    ].district.nunique()
    ws.cell(row=11, column=COL).value = len(data_school[data_school[TREATMENT] == 0])
    ws.cell(row=12, column=COL).value = data_school[
        data_school[TREATMENT] == 0
    ].district.nunique()

    wb.save(file)


for year, col in zip([2017, 2018, 2019], [2, 3, 4]):
    effect_input(
        outcome="teachers_uncertified",
        year=2017,
        treatment="exempt_certification",
        data=data_school[(data_school.year == YEAR) & (data_school.doi_year <= YEAR)],
        col=2,
    )
# %%
