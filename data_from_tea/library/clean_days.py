# %%
import pandas as pd
import numpy as np
import datetime
from dofis import start


# %%
def clean_cdays(year):

    if year < "yr1617":
        return pd.DataFrame()

    EARLIEST_START_DATE = {
        "yr1617": datetime.date(year=2016, month=8, day=14),
        "yr1718": datetime.date(year=2017, month=8, day=20),
        "yr1819": datetime.date(year=2018, month=8, day=19),
        "yr1920": datetime.date(year=2019, month=8, day=18),
        "yr2021": datetime.date(year=2016, month=8, day=16),
    }

    yr = year[4:6]

    TRACKS_LOCATION = start.DATA_PATH + "days/PRU_6691_ATTEND_TRACK_" + yr + ".csv"
    CALENDAR_LOCATION = start.DATA_PATH + "days/PRU_6691_CALENDAR_" + yr + ".csv"

    tracks = pd.read_csv(TRACKS_LOCATION)

    tracks = pd.DataFrame(
        tracks[["CAMPUS", "TRACK", "STUDENTS"]]
        .groupby(["CAMPUS", "TRACK"])
        .agg({"STUDENTS": "mean"})
    )
    tracks = tracks.reset_index().sort_values(by=["CAMPUS", "TRACK", "STUDENTS"])
    tracks = tracks.drop_duplicates(subset=["CAMPUS", "TRACK"], keep="first")

    calendar = pd.read_csv(CALENDAR_LOCATION)

    calendar = calendar.rename(columns={"SCHL_DAY_OPR_MIN": "SCHOOL_DAY_OPR_MINUTES"})

    df = tracks[["CAMPUS", "TRACK"]].merge(
        calendar, left_on=["CAMPUS", "TRACK"], right_on=["CAMPUS", "TRACK"], how="left"
    )

    # Calendar start date
    calendar_start_date = df[df.SIXWEEK == 1][["CAMPUS", "SIXWEEK_BEG_DT"]]
    calendar_start_date["days_start_date"] = pd.to_datetime(
        calendar_start_date.SIXWEEK_BEG_DT
    ).dt.date

    calendar_start_date["days_before_third_week"] = np.where(
        calendar_start_date.days_start_date < EARLIEST_START_DATE[year],
        1,
        0,
    )

    # Total school days
    total_school_days_in_sixweek = df.drop_duplicates(
        subset=["CAMPUS", "SIXWEEK"], keep="first"
    )

    total_school_days = pd.DataFrame(
        total_school_days_in_sixweek[["CAMPUS", "DAYS_TAUGHT"]]
        .groupby(["CAMPUS"])
        .agg({"DAYS_TAUGHT": "sum"})
    )

    # Total minutes

    total_school_minutes = pd.DataFrame(
        df[["CAMPUS", "SCHOOL_DAY_OPR_MINUTES"]]
        .groupby(["CAMPUS"])
        .agg({"SCHOOL_DAY_OPR_MINUTES": "sum"})
    )

    total_school_minutes["SCHOOL_DAY_OPR_MINUTES"] = np.where(
        total_school_minutes.SCHOOL_DAY_OPR_MINUTES <= 0,
        np.nan,
        total_school_minutes.SCHOOL_DAY_OPR_MINUTES,
    )

    total_school_minutes["minutes_less_than_minimum"] = np.where(
        total_school_minutes.SCHOOL_DAY_OPR_MINUTES < 75000, 1, 0
    )

    total_school_minutes["minutes_less_than_minimum"] = np.where(
        total_school_minutes.SCHOOL_DAY_OPR_MINUTES.isnull(),
        np.nan,
        total_school_minutes.minutes_less_than_minimum,
    )

    #
    final_df = calendar_start_date.merge(
        total_school_days, left_on="CAMPUS", right_on="CAMPUS"
    )
    final_df = final_df.merge(total_school_minutes, left_on="CAMPUS", right_on="CAMPUS")

    final_df = final_df.rename(
        columns={
            "CAMPUS": "campus",
            "DAYS_TAUGHT": "days",
            "SCHOOL_DAY_OPR_MINUTES": "minutes",
        }
    )

    final_df = final_df[
        [
            "campus",
            "days_start_date",
            "days_before_third_week",
            "days",
            "minutes",
            "minutes_less_than_minimum",
        ]
    ]

    final_df["days"] = np.where(final_df.days <= 0, np.nan, final_df.days)

    final_df["days_drop_outliers"] = np.where(
        final_df.days < 150, np.nan, final_df.days
    )

    final_df["minutes_drop_outliers"] = np.where(
        final_df.minutes < 40000, np.nan, final_df.minutes
    )

    final_df = final_df.drop_duplicates(subset="campus", keep="first")

    return final_df
