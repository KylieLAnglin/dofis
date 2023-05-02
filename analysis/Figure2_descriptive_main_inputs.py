import matplotlib.pyplot as plt
import pandas as pd

from dofis import start

plt.style.use("seaborn")
my_dpi = 96
plt.figure(figsize=(480 / my_dpi, 480 / my_dpi), dpi=my_dpi)

data = pd.read_csv(start.DATA_PATH + "clean/master_data_school.csv")
data = data[data.year >= 2016]
data = data[data.distischarter == 0]
data = data[data.campischarter == "N"]


def create_group_df(df, outcome):
    df["outcome"] = df[outcome]
    df = df[["year", "outcome"]]
    new_df = pd.DataFrame(df.groupby(["year"]).agg({"outcome": ["mean", "sem"]}))
    new_df = new_df.rename(columns={"mean": "score_mean", "sem": "score_se"})
    new_df["ub"] = new_df["outcome"]["score_mean"] + new_df["outcome"]["score_se"]
    new_df["lb"] = new_df["outcome"]["score_mean"] - new_df["outcome"]["score_se"]
    return new_df


title_labels = {
    "teacher_uncertified": "Proportion Uncertified Teachers",
    "teacher_out_of_field_fte": "Proportion Out-of-Field Teachers",
    "class_size_elem": "Average Elementary Class Size",
    "stu_teach_ratio": "Student-Teacher Ratio",
}

fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

subgroups = [
    ("All Schools", "solid"),
    ("Rural Schools", "dotted"),
    ("Q4 % Hispanic Students", "dashed"),
    ("Q4 % Black Students", "solid"),
    ("Q4 % FRPL Students", "dotted"),
]
# (0, (3,10,1,10))
for outcome, ax in zip(title_labels, [ax1, ax2, ax3, ax4]):
    df_average = create_group_df(df=data, outcome=outcome)
    df_rural = create_group_df(df=data[data.pre_rural == 1], outcome=outcome)
    df_urban = create_group_df(df=data[data.pre_urban == 1], outcome=outcome)
    df_black = create_group_df(df=data[data.pre_black100 == 1], outcome=outcome)
    df_hispanic = create_group_df(df=data[data.pre_hisp100 == 1], outcome=outcome)
    df_frpl = create_group_df(df=data[data.pre_frpl100 == 1], outcome=outcome)
    df_avescore = create_group_df(df=data[data.pre_avescore25 == 1], outcome=outcome)

    ax.set_prop_cycle(color=["black", "black", "black", "gray", "gray"])
    for i, (df, subgroup) in enumerate(
        zip(
            [
                df_average,
                df_rural,
                df_urban,
                df_black,
                df_hispanic,
                df_frpl,
            ],
            subgroups,
        )
    ):
        ax.plot(
            list(df.index),
            df["outcome"]["score_mean"],
            label=subgroup[0],
            linestyle=subgroup[1],
            linewidth=1.5 + i / 2,
        )

    ax.set_title(title_labels[outcome])
    ax.grid(False)

ax.legend(loc="lower left", bbox_to_anchor=(1, 0.5))

fig.savefig(start.TABLE_PATH + "trends_by_subgroup.pdf", bbox_inches="tight")
fig.savefig(start.TABLE_PATH + "formatted_results/Figure2.pdf", bbox_inches="tight")
