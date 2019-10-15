

import pandas as pd
import os
from data_from_tea.library import start

years = ['yr1213', 'yr1314', 'yr1415', 'yr1516', 'yr1617', 'yr1718']
for year in years:

    file = 'teacher_cert_' + year + '.csv'
    certification = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers', file))
    certification = certification.rename(columns = {'district': 'district_cert'})

    file = 'teacher_course_' + year + '.csv'
    assignments = pd.read_csv(os.path.join(start.data_path, 'tea', 'teachers', file))
    
    teachers = assignments.merge(certification, on = ['teacher_id'], how = 'left', indicator = '_merge')

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
    any_cert = teachers[['campus', 'certification']]
    any_cert = any_cert.groupby(['campus']).mean()

    # Elementary
    elem = teachers[(teachers.course_ela == True)]
    elem = elem[(elem.campus_elem == True)]
    elem = elem.groupby(['campus']).mean()
    elem = elem[['cert_area_elem']]


    # Secondary Math
    high_math = teachers[(teachers.course_math == True)]
    high_math = high_math[(high_math.campus_high == True)]
    high_math = high_math.groupby(['campus']).mean()
    high_math = high_math[['cert_secondary_math']]

    # Secondary Science
    high_sci = teachers[(teachers.course_science == True)]
    high_sci = high_sci[(high_sci.campus_high == True)]
    high_sci = high_sci.groupby(['campus']).mean()
    high_sci = high_sci[['cert_secondary_sci']]

    # Secondary ELA
    high_ela = teachers[(teachers.course_ela == True)]
    high_ela = high_ela[(high_ela.campus_high == True)]
    high_ela = high_ela.groupby(['campus']).mean()
    high_ela = high_ela[['cert_secondary_ela']]

    # CTE
    cte = teachers[(teachers.course_cte == True)]
    cte = cte[(cte.campus_elem == True)]
    cte = cte.groupby(['campus']).mean()
    cte = cte[['vocational', 'cert_area_voc']]

    # Merge to one dataset
    all_certs = any_cert.merge(elem, on = 'campus', how = 'left')
    all_certs = all_certs.merge(high_math, on = 'campus', how = 'left')
    all_certs = all_certs.merge(high_ela, on = 'campus', how = 'left')
    all_certs = all_certs.merge(high_sci, on = 'campus', how = 'left')
    all_certs = all_certs.merge(cte, on = 'campus', how = 'left', indicator = '_merge')
    
    # Add year variable
    years = {'yr1112': 2012,'yr1213': 2013, 'yr1314': 2014, 'yr1415': 2015, 'yr1516': 2016, 'yr1617':2017, 'yr1718': 2018, 'yr1819': 2019}
    all_certs['year'] = years[year]

    # Save
    file = 'teachers_' + year + '.csv'
    all_certs.to_csv(os.path.join(start.data_path, 'tea', 'teachers', file))


###
#   Append
###

certification_rates_yr1213 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_yr1213.csv')))
certification_rates_yr1314 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_yr1314.csv')))
certification_rates_yr1415 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_yr1415.csv')))
certification_rates_yr1516 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_yr1516.csv')))
certification_rates_yr1617 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_yr1617.csv')))
certification_rates_yr1718 = pd.read_csv((os.path.join(start.data_path, 'tea', 'teachers', 'teachers_yr1718.csv')))

certification_rates_long = pd.concat([certification_rates_yr1213, certification_rates_yr1314, certification_rates_yr1415, certification_rates_yr1516, certification_rates_yr1617, certification_rates_yr1718], sort=True)

certification_rates_long.to_csv((os.path.join(start.data_path, 'tea', 'certification_rates_long.csv')))


