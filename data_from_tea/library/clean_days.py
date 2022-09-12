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
        "yr2021": datetime.date(year=2020, month=8, day=15),
    }

    yr = year[4:6]

    TRACKS_LOCATION = start.DATA_PATH + "days/PRU_6691_ATTEND_TRACK_" + yr + ".csv"
    CALENDAR_LOCATION = start.DATA_PATH + "days/PRU_6691_CALENDAR_" + yr + ".csv"

    tracks = pd.read_csv(TRACKS_LOCATION)
    tracks["students"] = np.where(tracks.STUDENTS < 0, np.nan, tracks.STUDENTS)

    tracks = pd.DataFrame(
        tracks[["CAMPUS", "TRACK", "students"]]
        .groupby(["CAMPUS", "TRACK"])
        .agg({"students": "mean"})
    )
    tracks = tracks.reset_index().sort_values(
        by=["CAMPUS", "TRACK", "students"], ascending=False
    )
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
        df[["CAMPUS", "CALENDAR_DT", "SCHOOL_DAY_OPR_MINUTES"]]
        .groupby(["CAMPUS", "CALENDAR_DT"])
        .agg({"SCHOOL_DAY_OPR_MINUTES": "max"})
    )

    total_school_minutes = pd.DataFrame(
        total_school_minutes.groupby(["CAMPUS"]).agg({"SCHOOL_DAY_OPR_MINUTES": "sum"})
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

    # Average length school day

    average_school_minutes = pd.DataFrame(
        df[["CAMPUS", "CALENDAR_DT", "SCHOOL_DAY_OPR_MINUTES"]]
        .groupby(["CAMPUS", "CALENDAR_DT"])
        .agg({"SCHOOL_DAY_OPR_MINUTES": "max"})
    )

    average_school_minutes = pd.DataFrame(
        average_school_minutes.groupby(["CAMPUS"]).agg(
            {"SCHOOL_DAY_OPR_MINUTES": "mean"}
        )
    )

    average_school_minutes["SCHOOL_DAY_OPR_MINUTES"] = np.where(
        average_school_minutes.SCHOOL_DAY_OPR_MINUTES <= 0,
        np.nan,
        average_school_minutes.SCHOOL_DAY_OPR_MINUTES,
    )

    average_school_minutes = average_school_minutes.rename(
        columns={"SCHOOL_DAY_OPR_MINUTES": "SCHOOL_DAY_OPR_MINUTES_AVERAGE"}
    )
    average_school_minutes = average_school_minutes.reset_index()

    #
    final_df = calendar_start_date.merge(
        total_school_days, left_on="CAMPUS", right_on="CAMPUS"
    )
    final_df = final_df.merge(total_school_minutes, left_on="CAMPUS", right_on="CAMPUS")
    final_df = final_df.merge(
        average_school_minutes[["CAMPUS", "SCHOOL_DAY_OPR_MINUTES_AVERAGE"]],
        left_on="CAMPUS",
        right_on="CAMPUS",
    )

    final_df = final_df.rename(
        columns={
            "CAMPUS": "campus",
            "DAYS_TAUGHT": "days",
            "SCHOOL_DAY_OPR_MINUTES": "minutes",
            "SCHOOL_DAY_OPR_MINUTES_AVERAGE": "minutes_per_day",
        }
    )

    final_df = final_df[
        [
            "campus",
            "days_start_date",
            "days_before_third_week",
            "days",
            "minutes",
            "minutes_per_day",
            "minutes_less_than_minimum",
        ]
    ]

    final_df["days"] = np.where(final_df.days <= 0, np.nan, final_df.days)
    final_df["minutes"] = np.where(final_df.minutes <= 0, np.nan, final_df.minutes)
    final_df["minutes_per_day"] = np.where(
        final_df.minutes_per_day <= 0, np.nan, final_df.minutes_per_day
    )

    final_df["days_drop_outliers"] = np.where(
        final_df.days < 150, np.nan, final_df.days
    )

    final_df["minutes_drop_outliers"] = np.where(
        final_df.minutes < 40000, np.nan, final_df.minutes
    )

    final_df = final_df.drop_duplicates(subset="campus", keep="first")

    return final_df
