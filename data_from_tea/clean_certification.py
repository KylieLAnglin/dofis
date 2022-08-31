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

year = "yr1516"
teacher_datapath = start.DATA_PATH + "teachers/" + year + "/"


for year in ["yr1415", "yr1516", "yr1617", "yr1718", "yr1819", "yr2021", "yr2122"]:
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

    cert.to_csv(start.DATA_PATH + "teachers/cert_" + year + ".csv")
###
# %%
