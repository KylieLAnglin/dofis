import pandas as pd
import os
import fnmatch
import numpy as np
from library import start
from library import clean_tea

year = 'yr1718'

for year in ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1718']:
    # Read files
    folder = 'certification_' + year + '/'
    teacher_datapath = os.path.join(start.data_path, 'tea', 'teachers', folder)

    pattern = "TEACHER_MASTER*.TXT"
    teacher_files = []
    for entry in os.listdir(teacher_datapath):
        if fnmatch.fnmatch(entry, pattern):
            teacher_files.append(entry)
    teacher_files.sort()
    dirs_teachers = [teacher_datapath + file for file in teacher_files]
    df_list = [pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in dirs_teachers]
    teachers = pd.concat(df_list)
    teachers = teachers[teachers['ROLE NAME'] == 'TEACHER']

    vars_to_keep = {'SCRAMBLED UNIQUE ID': 'teacher_id', 'DISTRICT NUMBER': 'district', 'DISTRICT NAME': 'distname',
                    'CAMPUS NUMBER': 'campus', 'CAMPUS NAME': 'campname',
                    'CAMPUS GRADE GROUP NAME': 'camp_grade_group',
                    'FTE': 'fte', 'ROLE FULL TIME EQUIVALENT': 'fte_teacher',
                    'SUBJECT AREA NAME 1': 'sub_area1', 'SUBJECT AREA NAME 2': 'sub_area2',
                    'SUBJECT AREA NAME 3': 'sub_area3',
                    'SUBJECT AREA NAME 4': 'sub_area4', 'SUBJECT AREA NAME 5': 'sub_area5'}
    teachers = clean_tea.filter_and_rename_cols(teachers, vars_to_keep)
    teachers.head()

    teachers['campus_elem'] = np.where(
        (teachers.camp_grade_group == "ELEMENTARY") | (teachers.camp_grade_group == "ELEMENTARY / SECONDARY"), True, False)
    teachers['campus_middle'] = np.where(
        (teachers.camp_grade_group == "MIDDLE SCHOOL") | (teachers.camp_grade_group == "ELEMENTARY / SECONDARY"), True,
        False)
    teachers['campus_high'] = np.where(
        (teachers.camp_grade_group == "HIGH SCHOOL") | (teachers.camp_grade_group == "ELEMENTARY / SECONDARY"), True, False)

    teachers['course_elem'] = np.where(((teachers.sub_area1 == "SELF-CONTAINED") |
                                        (teachers.sub_area2 == "SELF-CONTAINED") |
                                        (teachers.sub_area3 == "SELF-CONTAINED") |
                                        (teachers.sub_area4 == "SELF-CONTAINED") |
                                        (teachers.sub_area5 == "SELF-CONTAINED")), True, False)
    teachers['course_math'] = np.where(((teachers.sub_area1 == "MATHEMATICS") |
                                        (teachers.sub_area2 == "MATHEMATICS") |
                                        (teachers.sub_area3 == "MATHEMATICS") |
                                        (teachers.sub_area4 == "MATHEMATICS") |
                                        (teachers.sub_area5 == "MATHEMATICS")), True, False)
    teachers['course_science'] = np.where(((teachers.sub_area1 == "SCIENCE") |
                                           (teachers.sub_area2 == "SCIENCE") |
                                           (teachers.sub_area3 == "SCIENCE") |
                                           (teachers.sub_area4 == "SCIENCE") |
                                           (teachers.sub_area5 == "SCIENCE")), True, False)
    teachers['course_cte'] = np.where(((teachers.sub_area1 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area2 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area3 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area4 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area5 == "CAREER & TECHNOLOGY EDUCATION")), True, False)

    teachers = teachers[
        ['teacher_id', 'district', 'campus', 'campus_elem', 'campus_middle', 'campus_high', 'course_elem', 'course_math',
         'course_science', 'course_cte']]

    teachers.sort_values(by=['teacher_id'], axis=0)
    filename = 'teacher_course_' + year + '.csv'
    teachers.to_csv(os.path.join(start.data_path, 'tea', 'teachers', filename))
