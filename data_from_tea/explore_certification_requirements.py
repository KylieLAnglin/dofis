# %%
import pandas as pd
from dofis.start import MAIN_PATH, DATA_PATH
from dofis.data_from_tea.library import build

pd.option_context("display.max_columns", None)
# %%
folder = MAIN_PATH + "Database on Certification Requirements from TEA/"

service_codes = pd.read_excel(folder + "Service_codes.xlsx")

# %%
year = "yr1718"
teacher_datapath = DATA_PATH + "teachers/" + year + "/"
pattern = "CERTIFICATION*.csv"  # CHANGE CHANGE CHANGE
cert = build.concat_files(path=teacher_datapath, pattern=pattern)
cert = cert[cert.ROLE_CREDENTIALED_FOR == "Teacher"]

cert["SUBJECT_AREA_LEVEL"] = cert.SUBJECT_AREA + " " + cert.CERTIFICATION_LEVEL
cert.SUBJECT_AREA_LEVEL.value_counts().head(20)

# %%
pattern = "TEACHER_MASTER*.TXT"
teachers = build.concat_files(path=teacher_datapath, pattern=pattern)
teachers = teachers[teachers["ROLE NAME"] == "TEACHER"]
teachers = teachers.rename(
    columns={"DISTRICT NAME": "district", "DISTRICT CITY": "city"}
)
teachers["SUBJECT AREA NAME 1"].value_counts().head(20)
teachers["LEVEL"] = teachers["CAMPUS LOW GRADE"] + " " + teachers["CAMPUS HIGH GRADE"]
teachers["SUBJECT_AREA_LEVEL"] = (
    teachers["SUBJECT AREA NAME 1"]
    + " "
    + teachers["CAMPUS LOW GRADE"]
    + " "
    + teachers["CAMPUS HIGH GRADE"]
)

# %%
pattern = "*CLASS*.TXT"
classes = build.concat_files(path=teacher_datapath, pattern=pattern)

# %%
big_df = teachers[
    [
        "CAMPUS GRADE GROUP CODE",
        "CAMPUS GRADE GROUP NAME",
        "SCRAMBLED UNIQUE ID",
        "ROLE NAME",
        "SUBJECT AREA NAME 1",
        "SUBJECT AREA NAME 2",
        "SUBJECT_AREA_LEVEL",
    ]
].merge(
    classes[
        [
            "SCRAMBLED UNIQUE ID",
            "CLASS NUMBER",
            "CLASS NAME",
            "CLASS TYPE CODE",
            "CLASS TYPE NAME",
            "SUBJECT AREA CODE",
            "SUBJECT AREA NAME",
            "SUBJECT CODE",
            "SUBJECT NAME",
            "GRADE LEVEL CODE",
            "GRADE LEVEL NAME",
            "ADVANCED COURSE",
        ]
    ],
    how="left",
    on="SCRAMBLED UNIQUE ID",
)

big_df = big_df.merge(
    cert, how="left", left_on="SCRAMBLED UNIQUE ID", right_on="PERSONID_SCRAM"
)

# %% General elementary

print(
    service_codes[
        service_codes.SERVICEX.str.lower().str.contains("elem")
    ].SERVICEX.value_counts()
)

# %%
