# %%
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl import load_workbook

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from linearmodels import PanelOLS
from openpyxl import load_workbook
from patsy import dmatrices


from dofis.analysis.library import start
from dofis.analysis.library import characteristics
from dofis.analysis.library import analysis


INPUTS = [
    "class_size_k",
    "class_size_1",
    "class_size_2",
    "class_size_3",
    "class_size_4",
    "class_size_5",
    "perf_attendance",
    "perf_stuattend",
    "perf_studays",
    "stu_teach_ratio",
    "days_max",
    "days_mean",
    "days_min",
    "teachers_certified",
    "teachers_uncertified",
    "teachers_secondary_math_certified",
    "teachers_secondary_math_uncertified",
    "teachers_secondary_math_outoffield",
    "teachers_secondary_science_outoffield",
    "teachers_secondary_science_uncertified",
    "teachers_secondary_cte_uncertified",
    "teachers_secondary_cte_outoffield",
]


COLUMNS = (
    ["year", "doi_year", "campus", "campname", "district", "distname"]
    + characteristics.POTENTIAL_COVARIATES
    + INPUTS
    + [
        "exempt_minutes",
        "exempt_certification",
        "exempt_classsize",
        "exempt_servicedays",
    ]
)

# %%
data_school = pd.read_csv(
    os.path.join(start.data_path, "clean", "gdid_school.csv"),
    sep=",",
    low_memory=False,
)
data_school = data_school[data_school.doi]
# data_school = data_school[COLUMNS]
data_school["const"] = 1

# %%
df = data_school.reset_index()
df["year"] = pd.to_datetime(df["year"], format="%Y")
# add column year to index
df = df.set_index(["year", "campus"])
# swap indexes
df.index = df.index.swaplevel(0, 1)
df[["district", "doi_year", "treatpost"]].sample(5)

# %%

event_study_model = (
    "class_size_5 ~ + 1 + pre5 + pre4 + pre3 + pre2 + "
    "post1 + post2 + post3 + EntityEffects"
)

mod = PanelOLS.from_formula(event_study_model, df)
res = mod.fit(cov_type="clustered", clusters=df.district)
nonparametric = []
nonparametric_se = []
for coef in ["pre5", "pre4", "pre3", "pre2", "pre1", "post1", "post2", "post3"]:
    nonpar = 0
    nonpar_se = 0
    if coef != "pre1":
        nonpar = res.params[coef]
        nonpar_se = res.std_errors[coef]
    nonparametric.append(nonpar)
    nonparametric_se.append(nonpar_se)
coef_df = pd.DataFrame(
    {
        "coef": nonparametric,
        "err": nonparametric_se,
        "year": [-5, -4, -3, -2, -1, 1, 2, 3],
    }
)
coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
coef_df["errsig"] = coef_df.err * 1.96

fig, ax = plt.subplots(figsize=(8, 5))

coef_df.plot(
    x="year", y="coef", kind="bar", ax=ax, color="none", yerr="errsig", legend=False
)
ax.set_ylabel("")
ax.set_xlabel("")
ax.scatter(
    x=pd.np.arange(coef_df.shape[0]),
    marker="s",
    s=120,
    y=coef_df["coef"],
    color="black",
)
ax.axhline(y=0, linestyle="--", color="black", linewidth=4)
ax.xaxis.set_ticks_position("none")
_ = ax.set_xticklabels(
    ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"], rotation=0
)
# ax.set_title('Impact on Student Achievement - Event Study Coefficients',
# fontsize = 16)

fig.savefig(start.table_path + "uncertified_event_study" + ".png", bbox_inches="tight")

# %%
