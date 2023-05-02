# %%
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

from dofis import start

# %%
subgroups = ["average", "rural", "hispanic", "black", "frpl"]
outcomes = [
    "math_yr15std",
    "reading_yr15std",
    "perf_attendance",
]

results = {}
for outcome in outcomes:
    results[outcome] = {}
    for subgroup in subgroups:
        results[outcome][subgroup] = {}

# %%
graph_parameters = {
    "average": {"x_ticks_location": -0.3, "color": "blue", "label": "Average Impact"},
    "rural": {"x_ticks_location": -0.1, "color": "green", "label": "Rural Schools"},
    "hispanic": {
        "x_ticks_location": 0,
        "color": "green",
        "label": "Q4 Schools by % Hispanic Students",
    },
    "black": {
        "x_ticks_location": 0.1,
        "color": "lightblue",
        "label": "Q4 Schools by % Black Students",
    },
    "frpl": {
        "x_ticks_location": 0.2,
        "color": "teal",
        "label": "Q4 Schools by % FRPL Students",
    },
    "math_yr15std": {
        "title": "Standardized Math Performance",
        "ylabel": "Effect Size",
        "ylim": (-0.5, 0.5),
    },
    "reading_yr15std": {
        "title": "Standardized Reading Performance",
        "ylabel": "Effect Size",
        "ylim": (-0.5, 0.5),
    },
    "perf_attendance": {
        "title": "Attendance Rate",
        "ylabel": "Average Percent Students Present",
        "ylim": (-10, 10),
    },
}


# %%
def coef_df(df: pd.DataFrame):
    coefs = []
    ses = []
    for year in df["agg.dynamic.egt"]:
        coef = df.loc[df["agg.dynamic.egt"] == year, "agg.dynamic.att.egt"]
        se = df.loc[df["agg.dynamic.egt"] == year, "agg.dynamic.se.egt"]
        coefs.append(coef)
        ses.append(se)

    coef_df = pd.DataFrame(
        {
            "coef": coefs,
            "err": ses,
            "year": list(df["agg.dynamic.egt"]),
        }
    )
    coef_df["lb"] = coef_df.coef - (1.96 * coef_df.err)
    coef_df["ub"] = coef_df.coef + (1.96 * coef_df.err)
    coef_df["errsig"] = coef_df.err * 1.96
    return coef_df


# %%
for subgroup in subgroups:
    results["math_yr15std"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_math_yr15std_" + subgroup + "_ag_raw.xlsx"
    )

    results["math_yr15std"][subgroup]["coef_df"] = coef_df(
        results["math_yr15std"][subgroup]["df"]
    )

    results["reading_yr15std"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_reading_yr15std_" + subgroup + "_ag_raw.xlsx"
    )

    results["reading_yr15std"][subgroup]["coef_df"] = coef_df(
        results["reading_yr15std"][subgroup]["df"]
    )

    results["perf_attendance"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_perf_attendance_" + subgroup + "_ag_raw.xlsx"
    )

    results["perf_attendance"][subgroup]["coef_df"] = coef_df(
        results["perf_attendance"][subgroup]["df"]
    )


# %%

fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)

for outcome, ax in zip(outcomes, [ax1, ax2, ax3, ]):
    colors = ["black", "dimgrey", "darkgrey", "dimgrey", "darkgrey"]
    linestyles = ["solid", "dotted", "dashed", "solid", "dotted"]
    markers = ["s", "o", "o", "v", "v"]
    for subgroup, color, marker in zip(subgroups, colors, markers):
        df = results[outcome][subgroup]["coef_df"]
        df = df[df.year >= -5]
        df["year"] = df.year.astype(int)

        xs = [x + graph_parameters[subgroup]["x_ticks_location"] for x in df["year"]]
        # color = graph_parameters[subgroup]["color"]

        for pos, y, err in zip(xs, df["coef"], df["errsig"]):
            eb1 = ax.errorbar(
                pos,
                y,
                err,
                lw=2,
                capsize=2,
                capthick=2,
                color=color,
                linestyle="--",
            )
            # eb1[-1][0].set_linestyle("--")

        ax.scatter(
            x=xs,
            marker=marker,
            s=30,
            y=df["coef"],
            color=color,
            label=graph_parameters[subgroup]["label"],
        )

    ax.axhline(y=0, linestyle="--", color="black", linewidth=1)
    ax.set_xticks(xs)
    ax.set_xticklabels(
        df["year"],
    )
    ax.set_ylabel(graph_parameters[outcome]["ylabel"])
    ax.set_title(graph_parameters[outcome]["title"])
    ax.axvline(linestyle="--", color="black", linewidth=1)
    ax.axvline(0, color="gray")

ax.legend(loc="lower left", bbox_to_anchor=(1, 0.5))

fig.savefig(start.TABLE_PATH + "formatted_results/Figure9.pdf", bbox_inches="tight")


# %%
