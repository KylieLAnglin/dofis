# %% Event Study Graphs - Math

mod = PanelOLS.from_formula("math" + EVENT_STUDY_MODEL, df)
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

# fig.savefig(start.table_path + "math_event_study" + ".png", bbox_inches="tight")
