import os
import pandas as pd
import numpy as np
from library import start
from merge_and_clean.library import clean_for_merge

try:
    from start import data_path
except ModuleNotFoundError:
    data_path = '/Users/kylieleblancKylie/domino/dofis/data/'



tea = pd.read_csv(os.path.join(start.data_path, 'tea', 'desc_c_long.csv'),
                  sep=",")
print(tea.columns)
#TODO add from district data: eligibility, geographic location (type, type_description)
#TODO calculate teacher tunover
tea = tea[['campus', 'campname', 'district', 'distname', 'distischarter', 'eligible', 'type', 'year',
           'cntyname', 'campischarter', 'rating_academic',
           'students_num', 'students_frpl_num',
           'students_black_num', 'students_hisp_num', 'students_white_num',
           'students_amind_num', 'students_asian_num', 'students_paci_num', 'students_tworaces_num',
           'teachers_num', 'teachers_new_num',
           'teachers_exp_ave', 'teachers_tenure_ave',
           'teachers_nodegree_num', 'teachers_badegree_num',
           'teachers_msdegree_num', 'teachers_phddegree_num',
           'r_3rd_avescore', 'r_3rd_numtakers',
           'm_3rd_avescore', 'm_3rd_numtakers',
           'r_4th_avescore', 'r_4th_numtakers',
           'm_4th_avescore', 'm_4th_numtakers',
           'r_5th_avescore', 'r_5th_numtakers',
           'm_5th_avescore', 'm_5th_numtakers',
           'r_6th_avescore', 'r_6th_numtakers',
           'm_6th_avescore', 'm_6th_numtakers',
           'r_7th_avescore', 'r_7th_numtakers',
           'm_7th_avescore', 'm_7th_numtakers',
           'r_8th_avescore', 'r_8th_numtakers',
           'm_8th_avescore', 'm_8th_numtakers',
           'alg_avescore', 'alg_numtakers',
           'bio_avescore', 'bio_numtakers',
           'eng1_avescore', 'eng1_numtakers',
           'eng2_avescore', 'eng2_numtakers',
           'us_avescore', 'us_numtakers']]

# Data from plans
laws = pd.read_csv(os.path.join(start.data_path, 'plans', 'doi_final.csv'),
                   sep=",")
laws = laws.drop(['Unnamed: 0', 'level', 'type', 'link', 'p_doi'],
                 axis=1)
laws = laws.rename({'district': 'distname'}, axis=1)
laws.head()


# Fix problems with district nams
# # Clean variables for merge

# problems with district name from scraping
tea = tea.pipe(clean_for_merge.resolve_unicode_problems, 'distname')
laws = laws.pipe(clean_for_merge.resolve_unicode_problems, 'distname')


# scraped names in title case, but tea all caps. change scraped distname to caps
laws = laws.pipe(clean_for_merge.uppercase_column, 'distname')

# sometimes districts named CISD othertimes ISD. Make all ISD
tea = clean_for_merge.replace_column_values(tea, 'distname', 'CISD', 'ISD')
laws = clean_for_merge.replace_column_values(laws, 'distname', 'CISD', 'ISD')


# fix district names that don't match
tea = clean_for_merge.sync_district_names(tea, 'distname')
laws = clean_for_merge.sync_district_names(laws, 'distname')

mismatch = clean_for_merge.get_not_in(laws, 'distname', tea, 'distname')
mismatch_list = clean_for_merge.strip_distnum_parens(list(mismatch.distname))

df = clean_for_merge.distnum_in_paren(
    tea[[elem in mismatch_list for elem in tea.distname]])

tea.loc[(tea['distname'].isin(mismatch_list)), 'distname'] = (
    tea.loc[(tea['distname'].isin(mismatch_list))]
        .pipe(clean_for_merge.distnum_in_paren)['distname']
)

# Merge
# # Merge
data = tea.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
data.loc[(data['_merge'] == 'both'), 'doi'] = True
data.loc[(data['_merge'] == 'left_only'), 'doi'] = False
data.head()


print(laws.distname.nunique(), tea.distname.nunique(), data.distname.nunique())

'students_amind_num', 'students_asian_num', 'students_paci_num', 'students_tworaces_num'

# # Convert strings to numeric
num_cols = ['students_num', 'students_frpl_num', 'students_black_num', 'students_white_num',
            'students_amind_num', 'students_asian_num', 'students_paci_num', 'students_tworaces_num',
            'teachers_nodegree_num', 'teachers_badegree_num', 'teachers_msdegree_num', 'teachers_phddegree_num',
            'teachers_num', 'teachers_exp_ave', 'teachers_tenure_ave']
data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')

 # Create variables


# Student characteristics

data['students_frpl'] = data['students_frpl_num'] / data['students_num']
data['students_black'] = data['students_black_num'] / data['students_num']
data['students_hisp'] = data['students_hisp_num'] / data['students_num']
data['students_white'] = data['students_white_num'] / data['students_num']


# Performance

# Standardize within subject using mean and standard deviation from 2014-15
data = clean_for_merge.standardize_scores(data=data, std_year='yr1415')
math_scores = ['m_3rd_std', 'm_4th_std', 'm_5th_std', 'm_6th_std', 'm_7th_std', 'm_8th_std']
reading_scores = ['r_3rd_std', 'r_4th_std', 'r_5th_std', 'r_6th_std', 'r_7th_std', 'r_8th_std']
all_scores = ['m_3rd_std', 'm_4th_std', 'm_5th_std', 'm_6th_std', 'm_7th_std', 'm_8th_std',
              'r_3rd_std', 'r_4th_std', 'r_5th_std', 'r_6th_std', 'r_7th_std', 'r_8th_std',
              'alg_std', 'bio_std', 'eng1_std', 'eng2_std', 'us_std']

data['math'] = data[math_scores].mean(axis=1)
data['reading'] = data[reading_scores].mean(axis=1)
data['avescores'] = data[all_scores].mean(axis=1)

# District Characteristics

geography = {'A': 'Urban', 'C': 'Urban',
             'B': 'Suburban', 'D': 'Suburban',
             'E': 'Town', 'F': 'Town', 'G': 'Town',
             'H': 'Rural'}
data['geography'] = data['type'].map(geography)

data['charter'] = np.where((data['distischarter'] == "Y"), True, False)

data['district_status'] = np.where((data['doi'] == False) & (data['charter'] == False), 'tps',
                            np.where((data['doi'] == True), 'doi',
                            np.where((data['charter'] == True), 'charter', 'missing')))

# Geography indicators
data['type_urban'] = np.where(data['geography'] == 'Urban', 1, 0)
data['type_suburban'] = np.where(data['geography'] == 'Suburban', 1, 0)
data['type_town'] = np.where(data['geography'] == 'Town', 1, 0)
data['type_rural'] = np.where(data['geography'] == 'Rural', 1, 0)

# Always eligible?
df_filter = data[['distname', 'year', 'eligible']]
df_filter = df_filter[~df_filter['year'].isin(['yr1112', 'yr1213', 'yr1314'])]
always_eligible = pd.DataFrame(df_filter.groupby(['distname'])['eligible'].min()).reset_index()
always_eligible.columns = ['distname', 'always_eligible']
data = data.merge(always_eligible.reset_index(), left_on='distname', right_on='distname', how='left')

#  Teacher Characteristics
data['teachers_nodegree'] = data['teachers_nodegree_num'] / data['teachers_num']
data['teachers_badegree'] = data['teachers_badegree_num'] / data['teachers_num']
data['teachers_msdegree'] = data['teachers_msdegree_num'] / data['teachers_num']
data['teachers_phddegree'] = data['teachers_phddegree_num'] / data['teachers_num']

# # Save
data.to_csv(os.path.join(start.data_path, 'data_from_tea', 'master_data_c.csv'),
            sep=",")

