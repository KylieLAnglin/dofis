# %%
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt

from dofis import start

# %%
subgroups = ["average", "rural", "hispanic", "black", "frpl"]
outcomes = [
    "teacher_uncertified",
    "teacher_out_of_field",
    "class_size_elem",
    "stu_teach_ratio",
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
    "teacher_uncertified": {
        "title": "Proportion Uncertified Teachers",
        "ylabel": "Proportion",
        "ylim": (-0.06, 0.06),
    },
    "teacher_out_of_field": {
        "title": "Proportion Out of Field Teachers",
        "ylabel": "Proportion",
        "ylim": (-0.06, 0.06),
    },
    "class_size_elem": {
        "title": "Average Elementary Class Size",
        "ylabel": "Students",
        "ylim": (-5, 5),
    },
    "stu_teach_ratio": {
        "title": "Student to Teacher Ratio",
        "ylabel": "Students",
        "ylim": (-5, 5),
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
    results["teacher_uncertified"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_uncertified_ag_raw_" + subgroup + ".xlsx"
    )

    results["teacher_uncertified"][subgroup]["coef_df"] = coef_df(
        results["teacher_uncertified"][subgroup]["df"]
    )

    results["teacher_out_of_field"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_out_of_field_ag_raw_" + subgroup + ".xlsx"
    )

    results["teacher_out_of_field"][subgroup]["coef_df"] = coef_df(
        results["teacher_out_of_field"][subgroup]["df"]
    )

    results["class_size_elem"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_class_size_elem_ag_raw_" + subgroup + ".xlsx"
    )

    results["class_size_elem"][subgroup]["coef_df"] = coef_df(
        results["class_size_elem"][subgroup]["df"]
    )

    results["stu_teach_ratio"][subgroup]["df"] = pd.read_excel(
        start.TABLE_PATH + "results_stu_teach_ratio_ag_raw_" + subgroup + ".xlsx"
    )

    results["stu_teach_ratio"][subgroup]["coef_df"] = coef_df(
        results["stu_teach_ratio"][subgroup]["df"]
    )


# %%


fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)


for outcome, ax in zip(outcomes, [ax1, ax2, ax3, ax4]):
    colors = ["black", "gray", "silver", "gray", "silver"]
    linestyles = ["solid", "dotted", "dashed", "solid", "dotted"]
    markers = ["o", "v", "v", "s", "s"]
    for subgroup, color, marker in zip(subgroups, colors, markers):
        df = results[outcome][subgroup]["coef_df"]
        df = df[df.year >= -5]

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
    # ax.set_xlim((-0.5, 7.5))
    ax.set_ylim(graph_parameters[outcome]["ylim"])
    ax.axvline(0, color="gray")

ax.legend(loc="lower left", bbox_to_anchor=(1, 0.5))
fig.savefig(start.TABLE_PATH + "formatted_results/Figure5.pdf", bbox_inches="tight")


# %%
