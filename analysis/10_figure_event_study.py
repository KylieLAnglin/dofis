# %% Event Study Graphs - Math
# %%
# %%
import pandas as pd
import numpy as np
import pandas as pd
from openpyxl import load_workbook
import scipy
import matplotlib.pyplot as plt

from dofis import start
from dofis.analysis.library import analysis

MATH_AGG = start.TABLE_PATH + "results_math_ag_raw.xlsx"
math_agg = pd.read_excel(MATH_AGG)

MATH_DISAG = start.TABLE_PATH + "results_math_disag_raw.xlsx"
math_disag = pd.read_excel(MATH_DISAG)

READING_AGG = start.TABLE_PATH + "results_reading_ag_raw.xlsx"
reading_agg = pd.read_excel(READING_AGG)

READING_DISAG = start.TABLE_PATH + "results_reading_disag_raw.xlsx"
reading_disag = pd.read_excel(READING_DISAG)

UNCERTIFIED_AGG = start.TABLE_PATH + "results_uncertified_ag_raw.xlsx"
uncertified_agg = pd.read_excel(UNCERTIFIED_AGG)

MATH_OUTOFFIELD = start.TABLE_PATH + "results_outoffield_math_ag_raw.xlsx"
math_outoffield_agg = pd.read_excel(MATH_OUTOFFIELD)

ELEM_CLASS_SIZE = start.TABLE_PATH + "results_class_size_elem_ag_raw.xlsx"
class_size_agg = pd.read_excel(ELEM_CLASS_SIZE)


data = pd.read_csv(start.DATA_PATH + "clean/r_data_school_2020_comparison.csv")
n = data.district.nunique()

# %%
# %%
def coef_df(df: pd.DataFrame):
    coefs = []
    ses = []
    for row in [0, 1, 2, 3, 4, 5, 6, 7]:
        coef = df.loc[row][3]
        se = df.loc[row][4]
        coefs.append(coef)
        ses.append(se)

    coef_df = pd.DataFrame(
        {
            "coef": coefs,
            "err": ses,
            "year": [-5, -4, -3, -2, -1, 1, 2, 3],
        }
    )
    coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
    coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
    coef_df["errsig"] = coef_df.err * 1.96
    return coef_df


def plot_study(coef_df: pd.DataFrame, title: str, ylabel: str, ylim: tuple = None):

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
        ["Pre5", "Pre4", "Pre3", "Pre2", "Pre1", "Post1", "Post2", "Post3"],
        rotation=0,
    )
    ax.set_xlabel("Time Point")
    ax.set_ylabel(ylabel)
    if ylim:
        ax.set_ylim(ylim)
    fig.savefig(start.TABLE_PATH + title + ".png", bbox_inches="tight")


df = coef_df(math_agg)
plot_study(coef_df=df, title="math_event_study", ylabel="Effect Size Estimate")


df = coef_df(uncertified_agg)
plot_study(
    coef_df=df,
    title="event_study_uncertified",
    ylabel="Effect on Proportion Teachers",
    ylim=(-0.05, 0.05),
)

df = coef_df(math_outoffield_agg)
plot_study(
    coef_df=df,
    title="event_study_outoffield_secondary_math",
    ylabel="Effect on Proportion Teachers",
)

df = coef_df(class_size_agg)
plot_study(
    coef_df=df,
    title="event_study_class_size_elem",
    ylabel="Effect on Average Class Size",
)
# %%
