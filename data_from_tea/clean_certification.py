# %%
import pandas as pd
import numpy as np

from dofis import start
from dofis.data_from_tea.library import build

# %% Cross walks
certification_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_certification.xlsx"
certification_crosswalk_df = pd.read_excel(
    certification_crosswalk_path, index_col="year"
)


certification_types_crosswalk_path = (
    start.DATA_PATH + "teachers/crosswalk_certification_types.xlsx"
)
certification_types_crosswalk_df = pd.read_excel(certification_types_crosswalk_path)


subject_areas_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_subject_areas.xlsx"
subject_areas_crosswalk = pd.read_excel(subject_areas_crosswalk_path)
subject_areas_crosswalk = dict(
    zip(
        subject_areas_crosswalk.original_subject_area,
        subject_areas_crosswalk.new_subject_area,
    )
)

grades_crosswalk_path = start.DATA_PATH + "teachers/crosswalk_grades.xlsx"
grades_crosswalk = pd.read_excel(grades_crosswalk_path, index_col="cert_grade")

# %%


def clean_certification(year):
    teacher_datapath = start.DATA_PATH + "teachers/" + year + "/"

    ###
    certification_crosswalk = certification_crosswalk_df.loc[year]
    certification_crosswalk = certification_crosswalk.to_dict()
    certification_crosswalk_invert = {v: k for k, v in certification_crosswalk.items()}

    cert = build.concat_files(
        path=teacher_datapath, pattern=certification_crosswalk["filepattern"]
    )
    cert = cert.rename(columns=certification_crosswalk_invert)
    cert = cert.loc[:, cert.columns.isin(list(certification_crosswalk.keys()))]

    certification_types_crosswalk = dict(
        zip(
            certification_types_crosswalk_df.cert_type,
            certification_types_crosswalk_df.certified,
        )
    )

    certification_types_crosswalk
    cert.cert_type.value_counts()
    cert["certified"] = cert["cert_type"].map(certification_types_crosswalk)

    subject_areas_crosswalk
    cert.cert_subject_area.value_counts()
    cert["subject"] = cert["cert_subject_area"].map(subject_areas_crosswalk)
    cert["subject"] = np.where(cert.cert_subject_area.isnull(), np.nan, cert.subject)
    cert["subject"] = np.where(
        cert.cert_subject == "Core Subjects", "elem", cert.subject
    )

    cert["cert_elem"] = np.where((cert.subject == "elem") & (cert.certified == 1), 1, 0)

    cert["cert_effective"] = cert["cert_effective"].astype(str)
    cert["cert_effective_year"] = [
        date[5:9] if date else "" for date in cert.cert_effective
    ]
    cert["cert_effective_yr"] = pd.to_numeric(cert["cert_effective_year"])

    cert["cert_expires"] = cert["cert_expires"].astype(str)
    cert["cert_expires_year"] = [
        date[5:9] if date else "" for date in cert.cert_expires
    ]
    cert["cert_expires_yr"] = np.where(
        cert.cert_expires_year == "", "3000", cert.cert_expires_year
    )
    cert["cert_expires_yr"] = pd.to_numeric(cert["cert_expires_yr"])

    cert["year"] = year
    # cert.to_csv(start.DATA_PATH + "teachers/cert_" + year + ".csv")

    cert["cert_active_2012"] = np.where(
        (cert.cert_effective_yr <= 2012) & (cert.cert_expires_yr > 2011), 1, 0
    )
    cert["cert_active_2013"] = np.where(
        (cert.cert_effective_yr <= 2013) & (cert.cert_expires_yr > 2012), 1, 0
    )
    cert["cert_active_2014"] = np.where(
        (cert.cert_effective_yr <= 2014) & (cert.cert_expires_yr > 2013), 1, 0
    )
    cert["cert_active_2015"] = np.where(
        (cert.cert_effective_yr <= 2015) & (cert.cert_expires_yr > 2014), 1, 0
    )
    cert["cert_active_2016"] = np.where(
        (cert.cert_effective_yr <= 2016) & (cert.cert_expires_yr > 2015), 1, 0
    )
    cert["cert_active_2017"] = np.where(
        (cert.cert_effective_yr <= 2017) & (cert.cert_expires_yr > 2016), 1, 0
    )
    cert["cert_active_2018"] = np.where(
        (cert.cert_effective_yr <= 2018) & (cert.cert_expires_yr > 2017), 1, 0
    )
    cert["cert_active_2019"] = np.where(
        (cert.cert_effective_yr <= 2019) & (cert.cert_expires_yr > 2018), 1, 0
    )
    cert["cert_active_2020"] = np.where(
        (cert.cert_effective_yr <= 2020) & (cert.cert_expires_yr > 2019), 1, 0
    )
    cert["cert_active_2021"] = np.where(
        (cert.cert_effective_yr <= 2021) & (cert.cert_expires_yr > 2020), 1, 0
    )

    return cert


data = clean_certification("yr1718")

# data["cert_effective"] = [date[0:9] for date in data.cert_effective]
# data["cert_effective_date"] = pd.to_datetime(data.cert_effective)

###
# %%
appended_data = []
for year in [
    "yr1213",
    "yr1314",
    "yr1415",
    "yr1516",
    "yr1617",
    "yr1718",
    "yr1819",
    "yr1920",
    "yr2021",
    "yr2122",
]:
    data = clean_certification(year)
    appended_data.append(data)

certification_database = pd.concat(appended_data)
certification_database.to_csv(start.DATA_PATH + "teachers/certifications_all.csv")
# %%
certifications = certification_database[
    [
        "teacher_id",
        "certified",
        "cert_grade",
        "cert_elem",
        "subject",
        "cert_active_2012",
        "cert_active_2013",
        "cert_active_2014",
        "cert_active_2015",
        "cert_active_2016",
        "cert_active_2017",
        "cert_active_2018",
        "cert_active_2019",
        "cert_active_2020",
        "cert_active_2021",
    ]
]
certifications_collapsed = (
    certifications.groupby(
        by=["teacher_id", "certified", "cert_grade", "subject", "cert_elem"],
        dropna=False,
    )
    .max()
    .reset_index()
)

certifications_collapsed.to_csv(start.DATA_PATH + "teachers/certifications_long.csv")
# %%
