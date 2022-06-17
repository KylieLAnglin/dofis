from typing import Optional

import pandas as pd
import numpy as np
import datetime


def prioritize_term_date(data: pd.DataFrame):
    """returns datetime for doi plan implementation

    if there is a term date, (i.e. "plan will be in effect \
        from August 2017 to August 2022") that date is preffered. \
        if no month is given, assume August. If no term date, \
        we use the date a plan was finalized (i.e. "August, 5, 2018 - \
        Board voted to approve DOI plan.")

    Args:
        data (pd.DataFrame): Dataframe which contains district name (distname)\
        term_year, term_month, finalize_year, and finalize month.

    Returns:
        [pd.DataFrame]: Contains district and doi datetime
    """
    dates = pd.DataFrame()

    dates["distname"] = data.distname
    dates["doi_year"] = data.term_year
    dates["doi_month"] = data.term_month
    dates.loc[
        (data["term_month"].isna()) & (~dates["doi_year"].isna()), "doi_month"
    ] = "August"

    # If missing, go with finalize date
    dates.loc[dates["doi_year"].isna(), "doi_month"] = data.finalize_month
    dates.loc[dates["doi_year"].isna(), "doi_year"] = data.finalize_year

    dates["day"] = 1
    months_dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    dates["month"] = dates["doi_month"].map(months_dict)
    dates["year"] = dates["doi_year"]
    dates["doi_date"] = pd.to_datetime(dates[["year", "month", "day"]])

    return dates


def next_month(date: datetime.datetime, month: int, day: int) -> int:
    """Get the year of the next month that matches passed argument

    Args:
        date (datetime.datetime): [current date]
        month (int): [month of interest]
        day (int): [day in month of interest]

    Returns:
        int: [year of month of interest]
    """
    # Treated if plan is implemented before March of year
    # (first possible testing date)
    if date.month < month or (date.month == month and date.day < day):
        return date.year
    return date.year + 1


def gen_vars(data):
    data = destring_vars(data)
    data = gen_exempt_categories(data)
    data = gen_student_vars(data)
    data = gen_district_vars(data)
    data = gen_teacher_vars(data)
    data = gen_score_vars(data)
    data = gen_gdid_vars(data)
    data = gen_event_vars(data)
    return data


def destring_vars(data):
    data["distischarter"] = np.where(data.distischarter == "Y", 1, 0)

    num_cols = [
        "teachers_nodegree_num",
        "teachers_badegree_num",
        "teachers_msdegree_num",
        "teachers_phddegree_num",
        "teachers_num",
        "teachers_exp_ave",
        "teachers_tenure_ave",
        "teachers_turnover_ratio_d",
        "stu_teach_ratio",
    ]
    for col in list(data.columns):
        if col.startswith("class_size") or col.startswith("perf"):
            num_cols.append(col)
    print(num_cols)
    data[num_cols] = data[num_cols].apply(pd.to_numeric, errors="coerce")

    return data


def gen_exempt_categories(data):
    data["exempt_firstday"] = np.where(data["reg25_0811"] == 1, 1, 0)
    data["exempt_minutes"] = np.where(data["reg25_081"] == 1, 1, 0)
    data["exempt_lastday"] = np.where(data["reg25_0812"] == 1, 1, 0)
    data["exempt_certification"] = np.where(
        (
            (data["reg21_003"] == 1)
            | (data["reg21_057"] == 1)
            | (data["reg21_053"] == 1)
        ),
        1,
        0,
    )
    data["exempt_probation"] = np.where(data["reg21_102"] == 1, 1, 0)
    data["exempt_servicedays"] = np.where(data["reg21_401"] == 1, 1, 0)
    data["exempt_eval"] = np.where(data["reg21_352"] == 1, 1, 0)
    data["exempt_classsize"] = np.where(
        ((data["reg25_112"] == 1) | (data["reg25_113"] == 1)), 1, 0
    )
    data["exempt_attendance"] = np.where(data["reg25_092"] == 1, 1, 0)
    data["exempt_behavior"] = np.where(data["reg37_0012"] == 1, 1, 0)

    return data


def gen_student_vars(data):
    data["students_frpl"] = data["students_frpl_num"] / data["students_num"]
    data["students_black"] = data["students_black_num"] / data["students_num"]
    data["students_hisp"] = data["students_hisp_num"] / data["students_num"]
    data["students_white"] = data["students_white_num"] / data["students_num"]
    data["students_ell"] = data["students_ell_num"] / data["students_num"]
    data["students_sped"] = data["students_sped_num"] / data["students_num"]
    # data["students_cte"] = data["students_cte_num"] / data["students_num"]

    data["days"] = data["perf_studays"] / data["students_num"]

    data["students_teacher_ratio"] = data.students_num / data.teachers_num

    return data


# District Characteristics


def gen_district_vars(data):
    data["charter"] = np.where((data["distischarter"] == "Y"), 1, 0)

    tps_districts = (data["doi"] is False) & (~data["charter"])

    data["district_status"] = np.where(
        tps_districts,
        "tps",
        np.where((data["doi"]), "doi", np.where((data["charter"]), "charter", "")),
    )

    # Geography indicators
    geography = {
        "A": "Urban",
        "C": "Urban",
        "B": "Suburban",
        "D": "Suburban",
        "E": "Town",
        "F": "Town",
        "G": "Town",
        "H": "Rural",
    }
    data["geography"] = data["type"].map(geography)
    data["type_urban"] = np.where(data["geography"] == "Urban", 1, 0)
    data["type_suburban"] = np.where(data["geography"] == "Suburban", 1, 0)
    data["type_town"] = np.where(data["geography"] == "Town", 1, 0)
    data["type_rural"] = np.where(data["geography"] == "Rural", 1, 0)

    data["eligible"] = np.where(
        (data.distischarter == "Y")
        | (data.rating_academic == "F")
        | (data.rating_financial == "Fail"),
        False,
        True,
    )

    return data


def gen_teacher_vars(data):
    #  Teacher Characteristics
    data["teachers_nodegree"] = data["teachers_nodegree_num"] / data["teachers_num"]
    data["teachers_badegree"] = data["teachers_badegree_num"] / data["teachers_num"]
    data["teachers_msdegree"] = data["teachers_msdegree_num"] / data["teachers_num"]
    data["teachers_phddegree"] = data["teachers_phddegree_num"] / data["teachers_num"]

    return data


def gen_certification_vars(data):
    certification_ratios = [
        {
            "new_var": "teachers_certified",
            "numerator": "teacher_certified",
            "denominator": "teachers",
        },
        {
            "new_var": "teachers_uncertified",
            "numerator": "teacher_uncertified",
            "denominator": "teachers",
        },
        {
            "new_var": "teachers_secondary_math_certified",
            "numerator": "teacher_secondary_math_certified",
            "denominator": "teacher_secondary_math",
        },
        {
            "new_var": "teachers_secondary_math_uncertified",
            "numerator": "teacher_secondary_math_uncertified",
            "denominator": "teacher_secondary_math",
        },
        {
            "new_var": "teachers_secondary_math_outoffield",
            "numerator": "teacher_secondary_math_outoffield",
            "denominator": "teacher_secondary_math",
        },
        {
            "new_var": "teachers_secondary_science_outoffield",
            "numerator": "teacher_secondary_science_outoffield",
            "denominator": "teacher_secondary_science",
        },
        {
            "new_var": "teachers_secondary_science_uncertified",
            "numerator": "teacher_secondary_science_uncertified",
            "denominator": "teacher_secondary_science",
        },
        {
            "new_var": "teachers_secondary_cte_uncertified",
            "numerator": "teacher_secondary_cte_uncertified",
            "denominator": "teacher_secondary_cte",
        },
        {
            "new_var": "teachers_secondary_cte_outoffield",
            "numerator": "teacher_secondary_cte_outoffield",
            "denominator": "teacher_secondary_cte",
        },
    ]
    for new_var_dict in certification_ratios:
        data[new_var_dict["new_var"]] = (
            data[new_var_dict["numerator"]] / data[new_var_dict["denominator"]]
        )

    return data


aggregate_variables = {
    "elem_math": ["m_3rd", "m_4th", "m_5th"],
    "elem_reading": ["r_3rd", "r_4th", "r_5th"],
    "elem": [
        "m_3rd",
        "m_4th",
        "m_5th",
        "r_3rd",
        "r_4th",
        "r_5th",
    ],
    "middle_math": ["m_6th", "m_7th", "m_8th"],
    "middle_reading": ["r_6th", "r_7th", "r_8th"],
    "middle_science": ["s_8th"],
    "algebra": ["alg"],
    "biology": ["bio"],
    "eng1": ["eng1"],
    "math": [
        "m_3rd",
        "m_4th",
        "m_5th",
        "m_6th",
        "m_7th",
        "m_8th",
        "alg",
    ],
    "reading": [
        "r_3rd",
        "r_4th",
        "r_5th",
        "r_6th",
        "r_7th",
        "r_8th",
        "eng1",
    ],
    "avescores": [
        "r_3rd",
        "m_3rd",
        "r_4th",
        "m_4th",
        "r_5th",
        "m_5th",
        "r_6th",
        "m_6th",
        "r_7th",
        "m_7th",
        "r_8th",
        "m_8th",
        "s_8th",
        "alg",
        "bio",
        "eng1",
        "eng2",
        "us",
    ],
}


def gen_score_vars(data):

    for col in aggregate_variables["avescores"]:
        old_var = col + "_avescore"
        new_var = col + "_std"
        data[new_var] = standardize_scores_within_year(
            data=data,
            year_column="year",
            score_column=old_var,
            test_column="",
            standardization_year=None,
        )

    for item in aggregate_variables:
        data[item] = data[[stub + "_std" for stub in aggregate_variables[item]]].mean(
            axis=1
        )

    for col in aggregate_variables["avescores"]:
        old_var = col + "_avescore"
        new_var = col + "_yr15std"
        data[new_var] = standardize_scores_within_year(
            data=data,
            year_column="year",
            score_column=old_var,
            test_column="",
            standardization_year=2015,
        )

    for item in aggregate_variables:
        data[item + "_yr15std"] = data[
            [stub + "_yr15std" for stub in aggregate_variables[item]]
        ].mean(axis=1)

    return data


def gen_eligiblity(
    data: pd.DataFrame,
    eligible_indicator: str,
    level: str,
    eligibility_year: int,
):
    """Generate eligibility indicator from eligibility year

    Args:
        data (pd.DataFrame): Dataframe containing years and eligibility indicator
        eligible_indicator (str): Column containing eligibility indicator
        level (str): campus or district
        eligibility_year (int): Year to use for eligibility
        new_var_name (str): name of new eligiblity variable from eligibility year

    Returns:
        [pd.Dataframe]: Data with new eligibility clolumn
    """

    datayear = data[data.year == eligibility_year]
    datayear = datayear[[level, eligible_indicator]]
    datayear = datayear.rename({eligible_indicator: "eligibility"}, axis=1)

    df = data.merge(
        datayear, how="left", left_on=[level], right_on=[level], validate="m:1"
    )
    return df.eligibility


def gen_analysis_sample(data: pd.DataFrame, min_doi_year: int, max_doi_year: int):
    """Generate indicator for whether district is in analytic sample based on implementation year

    Args:
        data (pd.DataFrame): Dataset for analyses
        min_doi_year (int): Exclude all dois that implement before this year
        max_doi_year (int): Exclude all dois that implement after this year

    Returns:
        list: list of indicators for whether in sample
    """

    df = data.copy()
    df["analytic_sample"] = np.where((df.doi == 1), 1, 0)
    df["analytic_sample"] = np.where(df.doi_year >= min_doi_year, df.analytic_sample, 0)
    df["analytic_sample"] = np.where(df.doi_year <= max_doi_year, df.analytic_sample, 0)

    return df.analytic_sample


def gen_analytic_group(data=pd.DataFrame):
    data["group"] = np.where(data.distischarter == 1, "charter", np.nan)
    data["group"] = np.where(
        ((data.distischarter == 0) & (data.doi == 0) & (data.eligible19)),
        "opt-out",
        data.group,
    )
    data["group"] = np.where(
        ((data.distischarter == 0) & (data.doi == 0) & (data.eligible19 == False)),
        "ineligible",
        data.group,
    )
    data["group"] = np.where(
        ((data.doi == 1) & (data.doi_year == 2017)),
        "2017",
        data.group,
    )
    data["group"] = np.where(
        ((data.doi == 1) & (data.doi_year == 2018)),
        "2018",
        data.group,
    )
    data["group"] = np.where(
        ((data.doi == 1) & (data.doi_year == 2019)),
        "2019",
        data.group,
    )
    data["group"] = np.where(
        ((data.doi == 1) & (data.doi_year == 2020)),
        "2020",
        data.group,
    )
    return data.group


# Specification variables
def gen_gdid_vars(data):
    data["treatpost"] = np.where(((data.year >= data.doi_year) & (data.doi)), 1, 0)
    data["yearpost"] = np.where(
        data.year >= data.doi_year, data.year - data.doi_year, 0
    )  # phase-in
    data["yearpre"] = np.where(
        data.year <= data.doi_year, data.year - data.doi_year, 0
    )  # pre-trend
    data["yearpre"] = np.where(data.yearpre <= -5, -5, data.yearpre)  # pre-trend effect
    return data


def gen_event_vars(data):
    # Non-parametric fixed effects for years pre and post - pre# and post#
    data["pre5"] = np.where(data.yearpre <= -5, 1, 0)
    data["pre4"] = np.where(data.yearpre == -4, 1, 0)
    data["pre3"] = np.where(data.yearpre == -3, 1, 0)
    data["pre2"] = np.where(data.yearpre == -2, 1, 0)
    data["pre1"] = np.where(data.yearpre == -1, 1, 0)
    data["post1"] = np.where((data.yearpost == 0) & (data.treatpost == 1), 1, 0)
    data["post2"] = np.where(data.yearpost == 1, 1, 0)
    data["post3"] = np.where(data.yearpost == 2, 1, 0)
    return data


def generate_pretreatment_variables(
    data: pd.DataFrame, level_index: str, pre_treatment_year: int
):
    """Merge descriptive statistics from pre-treatment year to all years

    Args:
        data (pd.DataFrame): data containing pre-treatment variables
        level_index (str): campus or district
        pre_treatment_year (int): pre-treatment year

    Returns:
        data: data with new columns
    """

    data_pre = data.loc[data.year == pre_treatment_year]
    data_pre = data_pre.rename(
        columns={
            "students_hisp": "pre_hisp",
            "students_ell": "pre_ell",
            "students_white": "pre_white",
            "students_black": "pre_black",
            "students_sped": "pre_sped",
            "students_frpl": "pre_frpl",
            "avescores": "pre_avescore",
            "students_num": "pre_num",
            "teachers_exp": "pre_exp",
            "teachers_turnover_ratio_d": "pre_turnover",
            "teachers_tenure_ave": "pre_tenure",
            "students_teacher_ratio": "pre_ratio",
        }
    )
    for var in [
        "pre_hisp",
        "pre_ell",
        "pre_white",
        "pre_black",
        "pre_sped",
        "pre_num",
        "pre_turnover",
        "pre_avescore",
    ]:
        for p in [0.25, 0.5, 0.75, 1]:
            num = str(int(p * 100))
            newvar = var + num
            if p == 0.25:
                data_pre[newvar] = np.where(
                    data_pre[var] <= data_pre[var].quantile(p), 1, 0
                )
            if p > 0.25:
                lp = p - 0.25
                data_pre[newvar] = np.where(
                    (
                        (data_pre[var] > data_pre[var].quantile(lp))
                        & (data_pre[var] <= data_pre[var].quantile(p))
                    ),
                    1,
                    0,
                )
    variables = [level_index]
    variables = variables + (list(data_pre.filter(regex=("pre_"))))
    data_pre = data_pre[variables]
    data_pre_geo_vars = [
        level_index,
        "type_urban",
        "type_suburban",
        "type_town",
        "type_rural",
    ]
    data_pre_geo = data[data.year == 2016][data_pre_geo_vars]
    data_pre = data_pre.merge(
        data_pre_geo,
        how="left",
        left_on=[level_index],
        right_on=[level_index],
        validate="one_to_one",
    )
    data_pre = data_pre.rename(
        columns={
            "type_urban": "pre_urban",
            "type_suburban": "pre_suburban",
            "type_town": "pre_town",
            "type_rural": "pre_rural",
        }
    )
    data_pre["pre_turnover"] = data_pre.pre_turnover / 100
    data = data.reset_index().merge(
        data_pre, left_on=level_index, right_on=level_index, how="left", validate="m:1"
    )

    return data


def standardize_scores_within_year(
    data: pd.DataFrame,
    year_column: str,
    score_column: str,
    test_column: str = "",
    standardization_year: Optional[int] = None,
):
    """Create list of scores standardized within year and test

    Args:
        data (pd.DataFrame): Dataframe containing score and year columns
        score_column (str): name of score column
        year_column (str): name of year column
        test_column (str): name of test column
        year ()


    Returns:
        list: list of standardized scores
    """
    df = data.copy()

    if test_column == "":
        df["test"] = "test"
        test_column = "test"

    df = df[[year_column, test_column, score_column]]
    df = df.rename(
        columns={score_column: "score", year_column: "year", test_column: "test"}
    )

    # zero degrees of freedom
    def std(x):
        return np.std(x)

    if standardization_year is None:
        statistics_df = df.groupby(["year", "test"]).agg(["mean", std], ddof=1)
        df = df.merge(statistics_df, how="left", on=["year", "test"])

    else:
        statistics_df = df[df.year == standardization_year]
        statistics_df = statistics_df.groupby(["year", "test"]).agg(
            ["mean", std], ddof=1
        )
        df = df.merge(statistics_df, how="left", on=["test"])

    df["score_std"] = (df["score"] - df[("score", "mean")]) / df[("score", "std")]

    return list(df.score_std)


# TODO: return list
def standardize_scores(data, std_year):
    yr_df = data[data.year == std_year]
    subjects = [
        "r_3rd",
        "m_3rd",
        "r_4th",
        "m_4th",
        "r_5th",
        "m_5th",
        "r_6th",
        "m_6th",
        "r_7th",
        "m_7th",
        "r_8th",
        "m_8th",
        "s_8th",
        "alg",
        "bio",
        "eng1",
        "eng2",
        "us",
    ]
    means = []
    sds = []
    for var in subjects:
        sub = var + "_avescore"
        mean = yr_df[sub].mean()
        means.append(mean)
        sd = yr_df[sub].std()
        sds.append(sd)

    for sub, mean, sd in zip(subjects, means, sds):
        old_var = sub + "_avescore"
        new_var = sub + "_std"
        data[new_var] = (data[old_var] - mean) / sd

    return data


def generate_district_spread(
    district_data: pd.DataFrame, school_data: pd.DataFrame, outcome: str, groupby: list
):
    """Generate variable indicating the distance between the highest and lowest performing school in the district

    Args:
        district_data (pd.DataFrame): Dataframe to merge to
        school_data (pd.DataFrame): Dataframe containing outcome variable
        outcome (str): Outcome variable to calculate spread
        groupby (list): List of variables to groupby (likely district and year)

    Returns:
        list: List of district spread values
    """
    district_statistics_df = school_data[[outcome] + groupby]
    district_statistics_df = district_statistics_df.groupby(groupby).agg(["min", "max"])

    district_df = district_data.merge(
        district_statistics_df, how="left", left_on=groupby, right_on=groupby
    )

    district_df["range"] = district_df[(outcome, "max")] - district_df[(outcome, "min")]

    return district_df.range
