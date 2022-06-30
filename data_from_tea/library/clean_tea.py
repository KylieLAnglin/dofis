import os
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import shutil

from dofis.start import DATA_PATH


def filter_and_rename_cols(df, mydict):
    """
    Keep some original cols from a dataframe, rename them to new column names
    Return a new data frame

    Arguments:
    df = data frame
    dict keys = original column names you want to keep
    dict values = new column names
    """
    df = df[list(mydict.keys())]
    new_df = df.rename(index=str, columns=mydict)
    return new_df


def fix_parser_error(input_path):
    """
    Some older datasets have observation data across two rows
    :param input_path: Location of data set
    :return: data set where columns are all in one row
    """
    temp_directory = os.path.join(DATA_PATH, "tea", "temp")
    temp_file = os.path.basename(input_path)
    temp_path = os.path.join(temp_directory, temp_file)

    print("Got a parser error - concatenating first two lines of text file to remedy!")
    shutil.copy(input_path, temp_path)

    with open(temp_path, "r") as file:
        text_contents = file.read()
    text_contents = text_contents.replace("\n", "", 1)
    with open(temp_path, "w") as file:
        file.write(text_contents)
    return temp_path


def clean_cref(year):
    """
    Reads district reference data from:
    https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    Manually add financial ratings from:
    https://tealprod.tea.state.tx.us/First/forms/Main.aspx

    :param year: year of data set to read
    :return: data frame with variables from dref to keep
    """

    if year == "yr1112":
        filename = "cref.dat"
    if year == "yr1213":
        filename = "CREF.txt"
    if year >= "yr1314" and year != "yr2021":
        filename = "CREF.dat"
    if year == "yr2021":
        filename = "CREF.csv"
    cref = pd.read_csv(os.path.join(DATA_PATH, "tea", "cref", year, filename), sep=",")
    # Note: no district number in early files
    cref_tokeep = {
        "DISTNAME": "distname",
        "CAMPUS": "campus",
        "CAMPNAME": "campname",
        "CFLCHART": "campischarter",
        "CNTYNAME": "cntyname_c",
        "GRDTYPE": "grade_range",
        "REGION": "region",
    }
    if year > "yr1112":
        cref_tokeep["C_RATING"] = "rating_academic_c"
    cref = filter_and_rename_cols(cref, cref_tokeep)
    if year == "yr2021":
        cref["campus"] = cref.campus.str.replace("'", "")
        cref["campus"] = cref.campus.astype("int")
    return cref


def clean_dtype(year):
    """
    https://tea.texas.gov/acctres/analyze/years.html
    """
    filename = "district" + year[2:6] + ".xls"
    sheetname = "district" + year[2:6]
    if year == "yr1718":
        sheetname = "2017-18 Data"
    if year == "yr1819":
        sheetname = "1819_Data"
    if year == "yr1920" or year == "yr2021":
        filename = "district1920.xlsx"
        sheetname = "1920_Data"
    xls = pd.ExcelFile(os.path.join(DATA_PATH, "tea", "dtype", filename))
    if year != "yr1718" and year != "yr1819":
        dtype = xls.parse(sheetname, skiprows=2)
        dtype_to_keep = {
            "District": "district",
            "Type": "type",
            "Description": "type_description",
        }
    if year == "yr1718" or year == "yr1819" or year == "yr1920" or year == "yr2021":
        dtype = xls.parse(sheetname)
        dtype_to_keep = {
            "District Number": "district",
            "TEA District Type": "type",
            "TEA Description": "type_description",
        }
    dtype = filter_and_rename_cols(dtype, dtype_to_keep)
    dtype = dtype.dropna(axis=0, subset=["district"])
    print("There are ", len(dtype), "districts in dtype")
    return dtype


def clean_cscores(year, subject):
    """
    Reads STAAR scores from
    https://tea.texas.gov/student.assessment/staar/aggregate/
    :param year: year to read
    :param subject: subject to read (see subject_dict keys for subjects
    :return:
    """
    # File name
    file_yr = year[4:6]
    subject_dict = {
        "3rd": "e3",
        "4th": "e4",
        "5th": "e5",
        "6th": "e6",
        "7th": "e7",
        "8th": "e8",
        "Algebra": "ea1",
        "Biology": "ebi",
        "EnglishI": "ee1",
        "EnglishII": "ee2",
        "USHistory": "eus",
    }
    file_sub = subject_dict[subject]
    file = "cfy" + file_yr + file_sub + ".dat"

    # English scores across two files in first years
    if year in ["yr1112", "yr1213"] and subject in ["EnglishI", "EnglishII"]:
        subject_dict = {"EnglishI": "ew1", "EnglishII": "ew2"}
        file = "cfy" + file_yr + subject_dict[subject] + ".dat"
        # need two files for early English scores (reading and writing) TODO: combine reading and writing
        try:
            cscores2 = pd.read_csv(
                os.path.join(DATA_PATH, "tea", "cscores", year, file), sep=","
            )
        except:
            new_path = fix_parser_error(
                os.path.join(DATA_PATH, "tea", "cscores", year, file)
            )
            cscores2 = pd.read_csv(new_path, sep=",")
        subject_dict = {"EnglishI": "er1", "EnglishII": "er2"}
        file = "cfy" + file_yr + subject_dict[subject] + ".dat"

    # Import dataa
    try:
        cscores = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "cscores", year, file), sep=","
        )
    except:
        new_path = fix_parser_error(
            os.path.join(DATA_PATH, "tea", "cscores", year, file)
        )
        cscores = pd.read_csv(new_path, sep=",")
    if subject not in [
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
    ]:
        return "invalid subject"
    if subject in ["3rd", "4th", "5th", "6th", "7th", "8th"]:
        cscores_tokeep = {
            "CAMPUS": "campus",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
        }
    if subject == "8th":
        cscores_tokeep["s_all_rs"] = "s_" + subject + "_avescore"
        cscores_tokeep["s_all_d"] = "s_" + subject + "_numtakers"
    if subject == "Algebra":
        cscores_tokeep = {
            "CAMPUS": "campus",
            "a1_all_rs": "alg_avescore",
            "a1_all_d": "alg_numtakers",
        }
        if year == "yr1819" or year == "yr2021":
            cscores_tokeep = {
                "campus": "campus",
                "a1_all_rs": "alg_avescore",
                "a1_all_d": "alg_numtakers",
            }
    if subject == "Biology":
        cscores_tokeep = {
            "CAMPUS": "campus",
            "bi_all_rs": "bio_avescore",
            "bi_all_d": "bio_numtakers",
        }
        if year == "yr1819" or year == "yr2021":
            cscores_tokeep = {
                "campus": "campus",
                "bi_all_rs": "bio_avescore",
                "bi_all_d": "bio_numtakers",
            }

    if subject == "EnglishI":
        if year == "yr1112" or year == "yr1213":
            cscores["e1_all_rs"] = cscores["r1_all_rs"] + cscores2["w1_all_rs"]
            cscores["e1_all_d"] = cscores["r1_all_d"]
        cscores_tokeep = {
            "CAMPUS": "campus",
            "e1_all_rs": "eng1_avescore",
            "e1_all_d": "eng1_numtakers",
        }
        if year == "yr1819" or year == "yr2021":
            cscores_tokeep = {
                "campus": "campus",
                "e1_all_rs": "eng1_avescore",
                "e1_all_d": "eng1_numtakers",
            }

    if subject == "EnglishII":
        if year == "yr1112" or year == "yr1213":
            cscores["e2_all_rs"] = cscores["r2_all_rs"] + cscores2["w2_all_rs"]
            cscores["e2_all_d"] = cscores["r2_all_d"]

        cscores_tokeep = {
            "CAMPUS": "campus",
            "e2_all_rs": "eng2_avescore",
            "e2_all_d": "eng2_numtakers",
        }
        if year == "yr1819" or year == "yr2021":
            cscores_tokeep = {
                "campus": "campus",
                "e2_all_rs": "eng2_avescore",
                "e2_all_d": "eng2_numtakers",
            }
    if subject == "USHistory":
        cscores_tokeep = {
            "CAMPUS": "campus",
            "us_all_rs": "us_avescore",
            "us_all_d": "us_numtakers",
        }
        if year == "yr1819" or year == "yr2021":
            cscores_tokeep = {
                "campus": "campus",
                "us_all_rs": "us_avescore",
                "us_all_d": "us_numtakers",
            }

    cscores = filter_and_rename_cols(cscores, cscores_tokeep)
    cscores["campus"] = cscores["campus"].apply(pd.to_numeric, errors="coerce")
    if year == "yr1112":
        cscores["campus"] = cscores["campus"].apply(int)
    cscores = cscores.set_index("campus")
    print("There are ", len(cscores), "schools in ", subject, "dataset.")
    return cscores


def clean_cdem(year):
    """
    Reads demographic data from TAPR reports: from
    https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html 2011-12 from AEIS reports
    https://rptsvr1.tea.texas.gov/perfreport/aeis/2012/index.html :param year: year of demographic data to read
    :return: data frame with variables from cdem to keep
    """

    if year == "yr1213":
        filename = "CAMPPROF.txt"
    elif year == "yr2021":
        filename = "CAMPPROF.csv"
    else:
        filename = "CAMPPROF.dat"
    cdem_tokeep = {
        "CAMPUS": "campus",
        # Teacher Characteristics
        "CPSTTOFC": "teachers_num",
        "CPST00FC": "teachers_new_num",
        "CPSTEXPA": "teachers_exp_ave",
        "CPSTTENA": "teachers_tenure_ave",
        "CPSTKIDR": "stu_teach_ratio",
        # Student Characteristics
        "CPETALLC": "students_num",
        "CPETECOC": "students_frpl_num",
        "CPETHISC": "students_hisp_num",
        "CPETWHIC": "students_white_num",
        "CPETBLAC": "students_black_num",
        "CPETINDC": "students_amind_num",
        "CPETASIC": "students_asian_num",
        "CPETPCIC": "students_paci_num",
        "CPETTWOC": "students_tworaces_num",
        "CPETLEPC": "students_ell_num",
        "CPETSPEC": "students_sped_num",
        # "CPETVOCC": "students_cte_num",
        # Class Sizes
        "CPCTGKGA": "class_size_k",
        "CPCTG01A": "class_size_1",
        "CPCTG02A": "class_size_2",
        "CPCTG03A": "class_size_3",
        "CPCTG04A": "class_size_4",
        "CPCTG05A": "class_size_5",
        "CPCTG06A": "class_size_6",
        "CPCTENGA": "class_size_sec_r",
        "CPCTFLAA": "class_size_sec_lang",
        "CPCTMATA": "class_size_sec_math",
        "CPCTSCIA": "class_size_sec_sci",
        "CPCTSOCA": "class_size_sec_ss",
    }
    # import data
    if year == "yr1112":
        cdem1 = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "cdem", year, "cstud.dat"), sep=","
        )
        cdem2 = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "cdem", year, "cstaf.dat"), sep=","
        )
        cdem = cdem1.merge(cdem2, on="CAMPUS", how="outer")
        cdem["CAMPUS"] = cdem["CAMPUS"].apply(int)
    else:
        cdem = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "cdem", year, filename), sep=","
        )
    # address variable name changes across years
    if year == "yr1112":
        cdem_tokeep["CPETALLC"] = "students_num"
    if year == "yr1213":
        cdem_tokeep["CPETALLC"] = "students_num"
    if year == "yr1314":
        cdem_tokeep["CPETALLC"] = "students_num"
    if year >= "yr1415":
        cdem_tokeep["CPETALLC"] = "students_num"
        cdem_tokeep["CPSTNOFC"] = "teachers_nodegree_num"
        cdem_tokeep["CPSTBAFC"] = "teachers_badegree_num"
        cdem_tokeep["CPSTMSFC"] = "teachers_msdegree_num"
        cdem_tokeep["CPSTPHFC"] = "teachers_phddegree_num"

    # filter and rename
    cdem = filter_and_rename_cols(cdem, cdem_tokeep)
    if year == "yr2021":
        cdem["campus"] = cdem.campus.str.replace("'", "")
    cdem["campus"] = cdem["campus"].apply(pd.to_numeric, errors="coerce")
    cdem["teachers_new_num"] = cdem["teachers_new_num"].apply(
        pd.to_numeric, errors="coerce"
    )

    cdem["teachers_num"] = cdem["teachers_num"].apply(pd.to_numeric, errors="coerce")
    to_num_cols = [
        "class_size_k",
        "class_size_1",
        "class_size_2",
        "class_size_3",
        "class_size_4",
        "class_size_5",
    ]
    cdem[to_num_cols] = cdem[to_num_cols].apply(pd.to_numeric, errors="coerce")
    cdem["class_size_elem"] = cdem[
        [
            "class_size_k",
            "class_size_1",
            "class_size_2",
            "class_size_3",
            "class_size_4",
            "class_size_5",
        ]
    ].mean(axis=1)

    print("There are ", len(cdem), "schools in cdem", year)
    return cdem


def clean_cgrad(year):
    # https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/cothr.html

    fallyr = year[2:4]  # next years data
    springyr = year[4:6]

    year = "yr" + str(int(fallyr) + 1) + str(int(springyr) + 1)

    year_files = {
        "yr1112": "CAMPPERF.dat",
        "yr1213": "CAMPPERF.txt",
        "yr1314": "CAMPPERF.dat",
        "yr1415": "CAMPPERF.dat",
        "yr1516": "CAMPPERF.dat",
        "yr1617": "CAMPPERF.dat",
        "yr1718": "CAMPGRAD.dat",
        "yr1819": "CAMPGRAD.dat",
        "yr1920": "CAMPGRAD.dat",
        "yr2021": "CAMPGRAD.csv",
    }

    cgrad = pd.read_csv(
        os.path.join(DATA_PATH, "tea", "cgrad", year, year_files[year]), sep=","
    )

    cgrad_to_keep = {
        "CAMPUS": "campus",
        "CA0AT" + springyr + "D": "perf_studays",
        "CA0AT" + springyr + "N": "perf_stuattend",
        "CA0AT" + springyr + "R": "perf_attendance",
        "CB0AT" + springyr + "R": "perf_attendance_black",
        "CE0AT" + springyr + "R": "perf_attendance_frpl",
        "CH0AT" + springyr + "R": "perf_attendance_hispanic",
        "CS0AT" + springyr + "R": "perf_attendance_sped",
        "CW0AT" + springyr + "R": "perf_attendance_white",
    }

    cgrad = filter_and_rename_cols(cgrad, cgrad_to_keep)

    if year == "yr1920":
        cgrad["campus"] = cgrad.campus.str.replace("'", "")
        cgrad["campus"] = cgrad.campus.astype("int")

    for var in list(cgrad.columns):
        cgrad[var] = cgrad[var].apply(pd.to_numeric, errors="coerce")
    # cgrad['campus'] = cgrad['campus'].apply(pd.to_numeric, errors='coerce')
    if year == "yr2021":
        cgrad = cgrad["campus"]

    return cgrad


def clean_dspending(year):
    springyr = year[4:6]
    springyr = "20" + springyr
    df_long = pd.read_csv(
        DATA_PATH + "tea/dspending/dspending/" + year + "/ACTget" + springyr + ".csv"
    )
    df_grouped = df_long.groupby(by=["DISTRICT", "FUNCTION"]).sum().reset_index()
    df_wide = df_grouped.pivot(index="DISTRICT", columns="FUNCTION", values="ACTAMT")

    spending = df_wide.reset_index()
    spending = spending.rename(
        columns={
            "DISTRICT": "district",
            11: "spending_instruction",
            23: "spending_admin",
        }
    )
    spending = spending[["district", "spending_instruction", "spending_admin"]]

    total = (
        df_long[["DISTRICT", "ACTAMT"]]
        .groupby(by=["DISTRICT"])
        .sum()
        .reset_index()
        .rename(columns={"DISTRICT": "district", "ACTAMT": "spending_total"})
    )

    spending = spending.merge(total, left_on="district", right_on="district")
    return spending


def clean_dgrad(year):
    # current year's values are stored in next year's dataset
    # https://rptsvr1.tea.texas.gov/perfreport/tapr/2013/download/dothr.html
    fallyr = year[2:4]
    springyr = year[4:6]
    nextyr = int(springyr) + 1

    data_year = "yr" + springyr + str(nextyr)

    if data_year < "yr1718":
        filename = "DISTPERF.dat"
    if data_year >= "yr1718":
        filename = "DISTGRAD.dat"
    if data_year == "yr1213":
        filename = "DISTPERF.txt"
    if data_year == "yr2021":
        filename = "DISTGRAD.csv"

    if data_year <= "yr1819":
        dgrad = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "dgrad", data_year, filename), sep=","
        )

        dgrad_to_keep = {
            "DISTRICT": "district",
            "DA0912DR" + springyr + "R": "perf_hsdrop",
            "DA0AT" + springyr + "D": "perf_studays",
            "DA0AT" + springyr + "N": "perf_stuattend",
            "DA0AT" + springyr + "R": "perf_attendance",
        }

        dgrad = filter_and_rename_cols(dgrad, dgrad_to_keep)
    if data_year >= "yr1920":
        dgrad = pd.DataFrame(
            columns=[
                "district",
                "perf_hsdrop",
                "perf_studays",
                "perf_stuattend",
                "perf_attendance",
            ]
        )
    return dgrad


def fix_duplicate_distname(df, distname_col="DISTNAME", cntyname_col="CNTYNAME"):
    dist_dict = [
        {
            "distname": "BIG SANDY ISD",
            "cntyname": "UPSHUR",
            "newname": "BIG SANDY ISD (230901)",
        },
        {
            "distname": "BIG SANDY ISD",
            "cntyname": "POLK",
            "newname": "BIG SANDY ISD (187901)",
        },
        {
            "distname": "CENTERVILLE ISD",
            "cntyname": "LEON",
            "newname": "CENTERVILLE ISD (145902)",
        },
        {
            "distname": "CENTERVILLE ISD",
            "cntyname": "TRINITY",
            "newname": "CENTERVILLE ISD (228904)",
        },
        {
            "distname": "CHAPEL HILL ISD",
            "cntyname": "TITUS",
            "newname": "CHAPEL HILL ISD (225906)",
        },
        {
            "distname": "CHAPEL HILL ISD",
            "cntyname": "SMITH",
            "newname": "CHAPEL HILL ISD (212909)",
        },
        {
            "distname": "DAWSON ISD",
            "cntyname": "NAVARRO",
            "newname": "DAWSON ISD (175904)",
        },
        {
            "distname": "DAWSON ISD",
            "cntyname": "DAWSON",
            "newname": "DAWSON ISD (58902)",
        },
        {
            "distname": "EDGEWOOD ISD",
            "cntyname": "BEXAR",
            "newname": "EDGEWOOD ISD (15905)",
        },
        {
            "distname": "EDGEWOOD ISD",
            "cntyname": "VAN ZANDT",
            "newname": "EDGEWOOD ISD (234903)",
        },
        {
            "distname": "HIGHLAND PARK ISD",
            "cntyname": "DALLAS",
            "newname": "HIGHLAND PARK ISD (57911)",
        },
        {
            "distname": "HIGHLAND PARK ISD",
            "cntyname": "POTTER",
            "newname": "HIGHLAND PARK ISD (188903)",
        },
        {
            "distname": "HUBBARD ISD",
            "cntyname": "BOWIE",
            "newname": "HUBBARD ISD (19913)",
        },
        {
            "distname": "HUBBARD ISD",
            "cntyname": "HILL",
            "newname": "HUBBARD ISD (109905)",
        },
        {
            "distname": "MIDWAY ISD",
            "cntyname": "MCLENNAN",
            "newname": "MIDWAY ISD (161903)",
        },
        {"distname": "MIDWAY ISD", "cntyname": "CLAY", "newname": "MIDWAY ISD (39905)"},
        {
            "distname": "NORTHSIDE ISD",
            "cntyname": "BEXAR",
            "newname": "NORTHSIDE ISD (15915)",
        },
        {
            "distname": "NORTHSIDE ISD",
            "cntyname": "WILBARGER",
            "newname": "NORTHSIDE ISD (244905)",
        },
        {
            "distname": "VALLEY VIEW ISD",
            "cntyname": "HIDALGO",
            "newname": "VALLEY VIEW ISD (108916)",
        },
        {
            "distname": "VALLEY VIEW ISD",
            "cntyname": "COOKE",
            "newname": "VALLEY VIEW ISD (49903)",
        },
        {"distname": "WYLIE ISD", "cntyname": "COLLIN", "newname": "WYLIE ISD (43914)"},
        {
            "distname": "WYLIE ISD",
            "cntyname": "TAYLOR",
            "newname": "WYLIE ISD (221912)",
        },
        {
            "distname": "RICHARD MILBURN ALTER HIGH SCHOOL",
            "cntyname": "BELL",
            "newname": "RICHARD MILBURN ALTER HIGH SCHOOL (14801)",
        },
        {
            "distname": "RICHARD MILBURN ALTER HIGH SCHOOL",
            "cntyname": "NUECES",
            "newname": "RICHARD MILBURN ALTER HIGH SCHOOL (178804)",
        },
    ]
    for entry in dist_dict:
        df.loc[
            (df[distname_col] == entry["distname"])
            & (df[cntyname_col] == entry["cntyname"]),
            distname_col,
        ] = entry["newname"]
    return df


def clean_cdays(year):
    """
    Reads number of schools days from dataset from PIR
    :param year:
    :return: renamed and filtered variables, with min, mean, and max by district
    Note: only available for yr1617 and 1718
    """
    filename = "days_" + year + ".csv"
    cdays = pd.read_csv(os.path.join(DATA_PATH, "tea", "cdays", filename), sep=",")
    cdays_to_keep = {
        "DISTRICT": "district",
        "CAMPUS": "campus",
        "TRACK": "track",
        "TOTAL_DAYS": "days",
    }
    cdays = filter_and_rename_cols(cdays, cdays_to_keep)
    cdays = cdays[["campus", "days"]]
    cdays = (
        cdays.groupby(by=["campus"]).agg({"days": ["min", "mean", "max"]}).reset_index()
    )
    cdays.columns = [" ".join(col).strip() for col in cdays.columns.values]
    cdays = cdays.rename(
        {"days min": "days_min", "days mean": "days_mean", "days max": "days_max"},
        axis="columns",
    )
    return cdays

    ####


def clean_dref(year):
    """
    Reads district reference data from:
    https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    Manually add financial ratings from:
    https://tealprod.tea.state.tx.us/First/forms/Main.aspx

    :param year: year of data set to read
    :return: data frame with variables from dref to keep

    """

    if year == "yr1112":
        filename = "DREF.csv"
    elif year == "yr1213":
        filename = "DREF.txt"
    elif year == "yr2021":
        filename = "DREF.csv"
    else:
        filename = "DREF.dat"
    dref = pd.read_csv(os.path.join(DATA_PATH, "tea", "dref", year, filename), sep=",")
    dref_tokeep = {
        "DISTRICT": "district",
        "DISTNAME": "distname",
        "DFLCHART": "distischarter",
        "CNTYNAME": "cntyname",
    }
    if year > "yr1112":
        dref_tokeep["D_RATING"] = "rating_academic"
    dref = filter_and_rename_cols(dref, dref_tokeep)
    if year == "yr1112":
        dref["district"] = dref["district"].str.strip("'")
        dref["district"] = dref["district"].apply(int)

    # Add financial rating (based on year before - https://tealprod.tea.state.tx.us/First/forms/Main.aspx)
    if year in ["yr1112", "yr1213", "yr1314"]:
        dref["rating_financial"] = None
    if year == "yr1415":
        failed_districts = [
            9901,
            59902,
            115902,
            123910,
            222901,
            242905,
            108914,
            14905,
            131001,
            84904,
            137904,
            237902,
        ]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year == "yr1516":
        failed_districts = [37908, 68901, 123910, 227907]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year == "yr1617":
        failed_districts = [92906, 163904, 174902, 70901, 7906]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year == "yr1718":
        failed_districts = [54901, 64903, 71903, 108902, 176902]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year == "yr1819":
        failed_districts = [
            18902,
            100908,
            101906,
            128901,
            133905,
            228905,
            57906,
            124901,
            152902,
            71903,
        ]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year == "yr1920":
        failed_districts = [
            18902,
            55901,
            128901,
            133905,
            177901,
            246913,
            247901,
            31911,
            124901,
        ]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year == "yr2021":
        dref["district"] = dref.district.str.replace("'", "")
        dref["district"] = dref.district.astype(int)
        failed_districts = [
            13901,
            55901,
            133905,
            246909,
            67906,
            31911,
            91902,
            91907,
            158904,
            222901,
        ]
        dref["rating_financial"] = np.where(
            (dref["district"].isin(failed_districts)), "Fail", "Pass"
        )
    if year not in ["yr1112", "yr1213", "yr1314"]:
        dref["eligible"] = np.where(
            (
                dref["rating_academic"].isin(["M", "A"])
                & (dref["rating_financial"] == "Pass")
                & (dref["distischarter"] == "N")
            ),
            True,
            False,
        )  # M= Meets standard, A = Meets alternative standard

    print("There are ", len(dref), "districts in dref")
    return dref


def clean_ddem(year):
    """
    Reads district level demographic data pulled from:
        https://rptsvr1.tea.texas.gov/perfreport/tapr/2017/download/DownloadData.html
    :param year: year of demographic data to read
    :return: data frame with variables from ddem to keep
    """

    if year == "yr1213":
        filename = "DISTPROF.txt"
    elif year == "yr2021":
        filename = "DISTPROF.csv"
    else:
        filename = "DISTPROF.dat"
    ddem_tokeep = {
        "DISTRICT": "district",
        # Teacher Characteristics
        "DPSTTOFC": "teachers_num",
        "DPSTKIDR": "stu_teach_ratio",
        "DPST00FC": "teachers_new_num",
        "DPSTEXPA": "teachers_exp_ave",
        "DPSTTENA": "teachers_tenure_ave",
        "DPSTURNR": "teachers_turnover_ratio_d",
        "DPSTNOFC": "teachers_nodegree_num",
        "DPSTBAFC": "teachers_badegree_num",
        "DPSTMSFC": "teachers_msdegree_num",
        "DPSTPHFC": "teachers_phddegree_num",
        # Student Characteristics
        "DPETALLC": "students_num",
        "DPETECOC": "students_frpl_num",
        "DPETHISC": "students_hisp_num",
        "DPETWHIC": "students_white_num",
        "DPETBLAC": "students_black_num",
        "DPETINDC": "students_amind_num",
        "DPETASIC": "students_asian_num",
        "DPETPCIC": "students_paci_num",
        "DPETTWOC": "students_tworaces_num",
        "DPETLEPC": "students_ell_num",
        "DPETSPEC": "students_sped_num",
        # "DPETVOCC": "students_cte_num",
        # Class Sizes
        "DPCTGKGA": "class_size_k",
        "DPCTG01A": "class_size_1",
        "DPCTG02A": "class_size_2",
        "DPCTG03A": "class_size_3",
        "DPCTG04A": "class_size_4",
        "DPCTG05A": "class_size_5",
        "DPCTG06A": "class_size_6",
        "DPCTENGA": "class_size_sec_r",
        "DPCTFLAA": "class_size_sec_lang",
        "DPCTMATA": "class_size_sec_math",
        "DPCTSCIA": "class_size_sec_sci",
        "DPCTSOCA": "class_size_sec_ss",
    }
    if year == "yr1112":
        ddem1 = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "ddem", year, "dstud.csv"), sep=","
        )
        ddem2 = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "ddem", year, "dstaf.csv"), sep=","
        )
        ddem = ddem1.merge(ddem2, on="DISTRICT", how="outer")
        ddem["DISTRICT"] = ddem["DISTRICT"].str.strip("'")
        ddem["DISTRICT"] = ddem["DISTRICT"].apply(int)
    else:
        ddem = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "ddem", year, filename), sep=","
        )
        ddem_tokeep["DPSTURND"] = "teachers_turnover_denom"
        ddem_tokeep["DPSTURNN"] = "teachers_turnover_num"
        ddem_tokeep["DPSTURNR"] = "teachers_turnover_ratio_d"
    ddem = filter_and_rename_cols(ddem, ddem_tokeep)
    ddem["teachers_num"] = pd.to_numeric(ddem.teachers_num, errors="coerce")
    ddem["teachers_new_num"] = pd.to_numeric(ddem.teachers_new_num, errors="coerce")

    if year == "yr2021":
        ddem["district"] = ddem.district.str.replace("'", "")
        ddem["district"] = ddem.district.astype("int")
    print("There are ", len(ddem), "districts in ddem")
    return ddem


def clean_scores(year, subject):
    """
    Reads STAAR scores from
    https://tea.texas.gov/Student_Testing_and_Accountability/Testing/State_of_Texas_Assessments_of_Academic_Readiness_(STAAR)/STAAR_Aggregate_Data_for_2017-2018/
    :param year: year to read
    :param subject: subject to read (see subject_dict keys for subjects
    :return:
    """
    file_yr = year[4:6]
    subject_dict = {
        "3rd": "e3",
        "4th": "e4",
        "5th": "e5",
        "6th": "e6",
        "7th": "e7",
        "8th": "e8",
        "Algebra": "ea1",
        "Biology": "ebi",
        "EnglishI": "ee1",
        "EnglishII": "ee2",
        "USHistory": "eus",
    }
    file_sub = subject_dict[subject]
    file = "dfy" + file_yr + file_sub + ".dat"

    if year in ["yr1112", "yr1213"] and subject in ["EnglishI", "EnglishII"]:
        subject_dict = {"EnglishI": "ew1", "EnglishII": "ew2"}
        file = "dfy" + file_yr + subject_dict[subject] + ".dat"
        # need two files for early English scores (reading and writing)
        try:
            dscores2 = pd.read_csv(
                os.path.join(DATA_PATH, "tea", "dscores", subject, file), sep=","
            )
        except:
            new_path = fix_parser_error(
                os.path.join(DATA_PATH, "tea", "dscores", subject, file)
            )
            dscores2 = pd.read_csv(new_path, sep=",")
        subject_dict = {"EnglishI": "er1", "EnglishII": "er2"}
        file = "dfy" + file_yr + subject_dict[subject] + ".dat"
    try:
        dscores = pd.read_csv(
            os.path.join(DATA_PATH, "tea", "dscores", subject, file), sep=","
        )
    except:
        new_path = fix_parser_error(
            os.path.join(DATA_PATH, "tea", "dscores", subject, file)
        )
        dscores = pd.read_csv(new_path, sep=",")

    variable_sets = {
        "3rd": {
            "DISTRICT": "district",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
        },
        "4th": {
            "DISTRICT": "district",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
        },
        "5th": {
            "DISTRICT": "district",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
            "s_all_rs": "s_" + subject + "_avescore",
            "s_all_d": "s_" + subject + "_numtakers",
        },
        "6th": {
            "DISTRICT": "district",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
        },
        "7th": {
            "DISTRICT": "district",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
        },
        "8th": {
            "DISTRICT": "district",
            "r_all_rs": "r_" + subject + "_avescore",
            "r_all_d": "r_" + subject + "_numtakers",
            "m_all_rs": "m_" + subject + "_avescore",
            "m_all_d": "m_" + subject + "_numtakers",
            "s_all_rs": "s_" + subject + "_avescore",
            "s_all_d": "s_" + subject + "_numtakers",
        },
        "Algebra": {
            "DISTRICT": "district",
            "a1_all_rs": "alg_avescore",
            "a1_all_d": "alg_numtakers",
        },
        "Biology": {
            "DISTRICT": "district",
            "bi_all_rs": "bio_avescore",
            "bi_all_d": "bio_numtakers",
        },
        "EnglishI": {
            "DISTRICT": "district",
            "e1_all_rs": "eng1_avescore",
            "e1_all_d": "eng1_numtakers",
        },
        "EnglishII": {
            "DISTRICT": "district",
            "e2_all_rs": "eng2_avescore",
            "e2_all_d": "eng2_numtakers",
        },
        "USHistory": {
            "DISTRICT": "district",
            "us_all_rs": "us_avescore",
            "us_all_d": "us_numtakers",
        },
    }

    if subject == "EnglishI":
        if year == "yr1112" or year == "yr1213":
            dscores["e1_all_rs"] = dscores["r1_all_rs"] + dscores2["w1_all_rs"]
            dscores["e1_all_d"] = dscores["r1_all_d"]

    if subject == "EnglishII":
        if year == "yr1112" or year == "yr1213":
            dscores["e2_all_rs"] = dscores["r2_all_rs"] + dscores2["w2_all_rs"]
            dscores["e2_all_d"] = dscores["r2_all_d"]

    dscores = filter_and_rename_cols(dscores, variable_sets[subject])
    if year == "yr1112":
        dscores["district"] = dscores["district"].apply(int)
    dscores = dscores.set_index("district")
    print("There are ", len(dscores), "districts in ", subject, "dataset.")
    # num_dups = len(dscores[dscores.index.duplicated(keep = False) == True])
    # print('There are', num_dups, ' duplicate indices.')

    return dscores


def clean_ddays(year):
    """
    Reads number of schools days from dataset from PIR
    :param year:
    :return: renamed and filtered variables, with min, mean, and max by district
    Note: only available for yr1617 and 1718
    """
    filename = "days_" + year + ".csv"
    cdays = pd.read_csv(os.path.join(DATA_PATH, "tea", "cdays", filename), sep=",")
    cdays_to_keep = {
        "DISTRICT": "district",
        "CAMPUS": "campus",
        "TRACK": "track",
        "TOTAL_DAYS": "days",
    }
    cdays = filter_and_rename_cols(cdays, cdays_to_keep)
    # No definition of tracks. So we keep the max number. May change later.
    cdays = cdays.groupby(by=["district", "campus"]).max().reset_index()
    ddays = (
        cdays.groupby(by=["district"])
        .agg({"days": ["min", "mean", "max"]})
        .reset_index()
    )
    ddays.columns = ["_".join(col).strip() for col in ddays.columns.values]
    ddays = ddays.rename(columns={"district_": "district"})

    return ddays
