import pandas as pd
import os
import fnmatch
import numpy as np
from library import start
from library import clean_tea

year = 'yr1718'

for year in ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']:

    # Concatenate Teacher Files for Year
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

    # Rename and Keep
    vars_to_keep = {'SCRAMBLED UNIQUE ID': 'teacher_id',
                    'DISTRICT NUMBER': 'district', 'DISTRICT NAME': 'distname',
                    'CAMPUS NUMBER': 'campus', 'CAMPUS NAME': 'campname',
                    'CAMPUS GRADE GROUP NAME': 'camp_grade_group',
                    'FTE': 'fte', 'ROLE FULL TIME EQUIVALENT': 'fte_teacher',
                    'SUBJECT AREA NAME 1': 'sub_area1', 'SUBJECT AREA NAME 2': 'sub_area2',
                    'SUBJECT AREA NAME 3': 'sub_area3',
                    'SUBJECT AREA NAME 4': 'sub_area4', 'SUBJECT AREA NAME 5': 'sub_area5',
                    'SUBJECT AREA NAME 6': 'sub_area6', 'SUBJECT AREA NAME 7': 'sub_area7',
                    'SUBJECT AREA NAME 8': 'sub_area8',
                    'SUBJECT AREA NAME 9': 'sub_area9', 'SUBJECT AREA NAME 10': 'sub_area10'
                    }
    teachers = clean_tea.filter_and_rename_cols(teachers, vars_to_keep)
    teachers.head()

    teachers['campus_elem'] = np.where((teachers.camp_grade_group == "ELEMENTARY"), True, False)
    teachers['campus_middle'] = np.where((teachers.camp_grade_group == "MIDDLE SCHOOL"), True, False)
    teachers['campus_high'] = np.where((teachers.camp_grade_group == "HIGH SCHOOL"), True, False)

    teachers['course_elem'] = np.where(((teachers.sub_area1 == "SELF-CONTAINED") |
                                        (teachers.sub_area2 == "SELF-CONTAINED") |
                                        (teachers.sub_area3 == "SELF-CONTAINED") |
                                        (teachers.sub_area4 == "SELF-CONTAINED") |
                                        (teachers.sub_area5 == "SELF-CONTAINED") |
                                        (teachers.sub_area5 == "SELF-CONTAINED") |
                                        (teachers.sub_area6 == "SELF-CONTAINED") |
                                        (teachers.sub_area7 == "SELF-CONTAINED") |
                                        (teachers.sub_area8 == "SELF-CONTAINED") |
                                        (teachers.sub_area9 == "SELF-CONTAINED") |
                                       (teachers.sub_area10 == "SELF-CONTAINED")) , True, False)

    teachers['course_math'] = np.where(((teachers.sub_area1 == "MATHEMATICS") |
                                        (teachers.sub_area2 == "MATHEMATICS") |
                                        (teachers.sub_area3 == "MATHEMATICS") |
                                        (teachers.sub_area4 == "MATHEMATICS") |
                                        (teachers.sub_area5 == "MATHEMATICS") |
                                        (teachers.sub_area6 == "MATHEMATICS") |
                                        (teachers.sub_area7 == "MATHEMATICS") |
                                        (teachers.sub_area8 == "MATHEMATICS") |
                                        (teachers.sub_area9 == "MATHEMATICS") |
                                        (teachers.sub_area10 == "MATHEMATICS")), True, False)
    teachers['course_science'] = np.where(((teachers.sub_area1 == "SCIENCE") |
                                           (teachers.sub_area2 == "SCIENCE") |
                                           (teachers.sub_area3 == "SCIENCE") |
                                           (teachers.sub_area4 == "SCIENCE") |
                                           (teachers.sub_area5 == "SCIENCE") |
                                           (teachers.sub_area6 == "SCIENCE") |
                                           (teachers.sub_area7 == "SCIENCE") |
                                           (teachers.sub_area8 == "SCIENCE") |
                                           (teachers.sub_area9 == "SCIENCE") |
                                           (teachers.sub_area10 == "SCIENCE")), True, False)
    teachers['course_ela'] = np.where(((teachers.sub_area1 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area2 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area3 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area4 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area5 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area6 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area7 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area8 == "ENGLISH LANGUAGE ARTS") |
                                           (teachers.sub_area9 == "ENGLISH LANGUAGE ARTS") |
                                            (teachers.sub_area10 == "ENGLISH LANGUAGE ARTS")), True, False)

    teachers['course_cte'] = np.where(((teachers.sub_area1 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area2 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area3 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area4 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area5 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area6 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area7 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area8 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area9 == "CAREER & TECHNOLOGY EDUCATION") |
                                       (teachers.sub_area10 == "CAREER & TECHNOLOGY EDUCATION")), True, False)

    teachers = teachers[
        ['teacher_id', 'district', 'campus', 'campus_elem', 'campus_middle', 'campus_high',
        'course_ela', 'course_elem', 'course_math', 'course_science', 'course_cte']]

    teachers.sort_values(by=['teacher_id'], axis=0)
    filename = 'teachers_' + year + '.csv'
    teachers.to_csv(os.path.join(start.data_path, 'tea', 'teachers', filename))
