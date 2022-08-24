# %%
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import datetime
from dofis import start

# %%
tracks = pd.read_csv(start.DATA_PATH + "PIR School Days/PRU_6691_ATTEND_TRACK_17.csv")

tracks = pd.DataFrame(
    tracks[["CAMPUS", "TRACK", "STUDENTS"]]
    .groupby(["CAMPUS", "TRACK"])
    .agg({"STUDENTS": "mean"})
)
tracks = tracks.reset_index().sort_values(by=["CAMPUS", "TRACK", "STUDENTS"])
tracks = tracks.drop_duplicates(subset=["CAMPUS", "TRACK"], keep="first")
# %%
calendar = pd.read_csv(start.DATA_PATH + "PIR School Days/PRU_6691_CALENDAR_17.csv")

df = tracks[["CAMPUS", "TRACK"]].merge(
    calendar, left_on=["CAMPUS", "TRACK"], right_on=["CAMPUS", "TRACK"], how="left"
)

# %% Calendar start date
calendar_start_date = df[df.SIXWEEK == 1][["CAMPUS", "SIXWEEK_BEG_DT"]]
calendar_start_date["days_start_date"] = pd.to_datetime(
    calendar_start_date.SIXWEEK_BEG_DT
).dt.date

calendar_start_date["days_before_third_week"] = np.where(
    calendar_start_date.school_start_date < datetime.date(year=2016, month=8, day=14),
    1,
    0,
)  # less than August 14


# %% Total school days

total_school_days_in_sixweek = df.drop_duplicates(
    subset=["CAMPUS", "SIXWEEK"], keep="first"
)

total_school_days = pd.DataFrame(
    total_school_days_in_sixweek[["CAMPUS", "DAYS_TAUGHT"]]
    .groupby(["CAMPUS"])
    .agg({"DAYS_TAUGHT": "sum"})
)
# %% Total minutes

total_school_minutes = pd.DataFrame(
    df[["CAMPUS", "SCHOOL_DAY_OPR_MINUTES"]]
    .groupby(["CAMPUS"])
    .agg({"SCHOOL_DAY_OPR_MINUTES": "sum"})
)

total_school_minutes["minutes_less_than_minimum"] = np.where(
    total_school_minutes.SCHOOL_DAY_OPR_MINUTES < 75000, 1, 0
)

# %%
final_df = calendar_start_date.merge(
    total_school_days, left_on="CAMPUS", right_on="CAMPUS"
)
final_df = final_df.merge(total_school_minutes, left_on="CAMPUS", right_on="CAMPUS")

final_df = final_df.rename(
    columns={"DAYS_TAUGHT": "days", "SCHOOL_DAY_OPR_MINUTES": "minutes"}
)

final_df = final_df[
    [
        "CAMPUS",
        "days_start_date",
        "days_before_third_week",
        "days",
        "minutes",
        "minutes_less_than_minimum",
    ]
]


# %%
