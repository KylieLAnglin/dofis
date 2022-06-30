import pandas as pd
import os
from dofis.start import DATA_PATH
from dofis.data_from_tea.library import clean_tea

years = [
    # "yr1112",
    # "yr1213",
    # "yr1314",
    # "yr1415",
    # "yr1516",
    # "yr1617",
    # "yr1718",
    # "yr1819",
    "yr1920",
    # "yr2021",
]
for year in years:
    print(year)
    # distname, campus, campname, campischarter, cntyname_c, grade_range, region, academic rating
    cref = clean_tea.clean_cref(year=year)
    cref = clean_tea.fix_duplicate_distname(
        cref, distname_col="distname", cntyname_col="cntyname_c"
    )

    # add district number and district academic and financial rating
    dref = clean_tea.clean_dref(year=year)
    dref = clean_tea.fix_duplicate_distname(
        dref, distname_col="distname", cntyname_col="cntyname"
    )

    # rural, urbam, suburban
    dtype = clean_tea.clean_dtype(year=year)

    cgrad = clean_tea.clean_cgrad(year=year)

    # student and teacher characteristics
    cdem = clean_tea.clean_cdem(year=year)
    ddem = clean_tea.clean_ddem(year=year)  # number of students in district
    ddem_tokeep = {
        "district": "district",
        "students_num": "students_num_d",
        "teachers_turnover_ratio_d": "teachers_turnover_ratio_d",
    }
    ddem = clean_tea.filter_and_rename_cols(ddem, ddem_tokeep)

    # test scores
    if year != "yr1920":
        cscores = pd.DataFrame(columns=["campus"])

        subjects = [
            "3rd",
            "4th",
            "5th",
            "6th",
            "7th",
            "8th",
            "Algebra",
            "Biology",
            "EnglishI",
            "EnglishII",
            "USHistory",
        ]
        for subject in subjects:
            cscores_subject = clean_tea.clean_cscores(year, subject)
            cscores = cscores.merge(cscores_subject, how="outer", on="campus")
    descriptives = cref.merge(dref, on="distname", how="inner", validate="m:1")
    descriptives["district"] = descriptives.district.astype("int")
    descriptives = descriptives.merge(dtype, on="district", how="inner", validate="m:1")
    descriptives = descriptives.merge(cgrad, on="campus", how="left", validate="1:1")
    descriptives = descriptives.merge(cdem, on="campus", how="left", validate="1:1")
    descriptives = descriptives.merge(ddem, on="district", how="inner", validate="m:1")
    if year != "yr1920":
        descriptives = descriptives.merge(
            cscores, on="campus", how="left", indicator=True, validate="1:1"
        )
    descriptives = descriptives.dropna(how="all")

    # days
    if year == "yr1617" or year == "yr1718":
        cdays = clean_tea.clean_cdays(year)
        descriptives = descriptives.merge(
            cdays, on="campus", how="left", validate="1:1"
        )
        print(len(descriptives))

    year_map = {
        "yr1112": 2012,
        "yr1213": 2013,
        "yr1314": 2014,
        "yr1415": 2015,
        "yr1516": 2016,
        "yr1617": 2017,
        "yr1718": 2018,
        "yr1819": 2019,
        "yr1920": 2020,
        "yr2021": 2021,
    }
    descriptives["year"] = year_map[year]
    yr_file = "desc_c_" + year + ".csv"

    descriptives.to_csv((os.path.join(DATA_PATH, "tea", yr_file)))
