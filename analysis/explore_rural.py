# %%
import pandas as pd
import numpy as np
from dofis import start
import statsmodels.formula.api as smf
import statsmodels.api as sm

from dofis.analysis.library import analysis

# %%
data = pd.read_csv(start.DATA_PATH + "clean/r_data.csv")
data = data[data.year < 2020]
pd.crosstab(data.type_description, data.pre_rural)

data = data[data.pre_rural == 1]

len(data[(data.year == 2016) | (data.year == 2019)])
data[(data.year == 2016) | (data.year == 2019)].campus.nunique()


limited_data = analysis.simple_did_df(
    group_var="group", group=2017, time_var="year", time=2019, df=data
)


df = data[(data.year == 2016) | (data.year == 2019)]
df["treat"] = np.where(df.group == "2017", 1, 0)
df["post"] = np.where(df.year > 2016, 1, 0)
df["treat_post"] = df.treat * df.post
df = df[df.group.isin(["2017", "2018", "2019", "2020+"])]

mod = smf.ols("math_yr15std" + " ~ 1 + treat + post + treat_post", df)
res = mod.fit(cov_type="cluster", cov_kwds={"groups": df["district"]})
res.summary()

mod = smf.ols(
    "math_yr15std"
    + " ~ 1 + treat + post + treat_post + pre_num + pre_hisp + pre_white + pre_frpl + pre_avescore",
    limited_data,
)
res = mod.fit(cov_type="cluster", cov_kwds={"groups": limited_data["district"]})
res.summary()

# %%
