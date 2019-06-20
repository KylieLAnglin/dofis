

import pandas as pd
import os
from library import start


file = 'teacher_cert_yr1718.csv'
certification = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers', file))

file = 'teacher_course_yr1718.csv'
assignments = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers', file))


teachers = assignments.merge(certification, on = ['teacher_id', 'district'], how = 'left', indicator = '_merge')
teachers[teachers.teacher_id == 'Q3Q2QF*48']


teachers['certification'] = teachers.certification.astype(bool)
teachers['vocational'] = teachers.vocational.astype(bool)
teachers['cert_elem'] = teachers.cert_elem.astype(bool)
teachers['cert_middle'] = teachers.cert_middle.astype(bool)
teachers['cert_high'] = teachers.cert_high.astype(bool)
teachers['cert_area_elem'] = teachers.cert_area_elem.astype(bool)
teachers['cert_area_ela'] = teachers.cert_area_ela.astype(bool)
teachers['cert_area_math'] = teachers.cert_area_math.astype(bool)
teachers['cert_area_sci'] = teachers.cert_area_sci.astype(bool)
teachers['cert_area_voc'] = teachers.cert_area_voc.astype(bool)
teachers['cert_secondary_ela'] = teachers.cert_secondary_ela.astype(bool)
teachers['cert_secondary_sci'] = teachers.cert_secondary_sci.astype(bool)
teachers['cert_secondary_math'] = teachers.cert_secondary_math.astype(bool)



teachers._merge.value_counts()

# Any Certification
any_cert = teachers[['district', 'certification']]
any_cert = any_cert.groupby(['district']).mean()

# Elementary
elem = teachers[(teachers.course_ela == True)]
elem = elem[(elem.campus_elem == True)]
elem = elem.groupby(['district']).mean()
elem = elem[['cert_area_elem']]


# Secondary Math
high_math = teachers[(teachers.course_math == True)]
high_math = high_math[(high_math.campus_high == True)]
high_math = high_math.groupby(['district']).mean()
high_math = high_math[['cert_secondary_math']]

# Secondary Science
high_sci = teachers[(teachers.course_science == True)]
high_sci = high_sci[(high_sci.campus_high == True)]
high_sci = high_sci.groupby(['district']).mean()
high_sci = high_sci[['cert_secondary_sci']]

# Secondary ELA
high_ela = teachers[(teachers.course_ela == True)]
high_ela = high_ela[(high_ela.campus_high == True)]
high_ela = high_ela.groupby(['district']).mean()
high_ela = high_ela[['cert_secondary_ela']]

# CTE
cte = teachers[(teachers.course_cte == True)]
cte = cte[(cte.campus_elem == True)]
cte = cte.groupby(['district']).mean()
cte = cte[['vocational', 'cert_area_voc']]

