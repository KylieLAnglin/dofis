import pandas as pd
import os
from library import start
from library import clean_for_merge

tea = pd.read_csv(os.path.join(start.data_path, 'tea', 'desc_long.csv'),
                  sep=",")
print(tea.columns)
tea = tea[['district', 'distname', 'year',
           'cntyname', 'distischarter', 'rating',
           'type', 'type_description',
           'students_num', 'students_frpl_num',
           'students_black_num', 'students_hisp_num', 'students_white_num',
           'teachers_num', 'teachers_new_num', 'teacher_turnover_num',
           'teachers_turnover_denom', 'teachers_turnover_ratio',
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

laws = pd.read_csv(os.path.join(start.data_path, 'plans', 'doi_final.csv'),
                   sep=",")
laws = laws.drop(['Unnamed: 0', 'level', 'type', 'link', 'p_doi', 'date_p'],
                 axis=1)
laws = laws.rename({'district': 'distname'}, axis=1)
laws.head()

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
tea.head()
laws.head()

# # Merge
data = tea.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
data.loc[(data['_merge'] == 'both'), 'doi'] = True
data.loc[(data['_merge'] == 'left_only'), 'doi'] = False
data.head()

laws.distname.nunique(), tea.distname.nunique(), data.distname.nunique()


# # Create variables


# # Save

data.to_csv(os.path.join(start.data_path, 'clean', 'master_data.csv'),
            sep=",")
