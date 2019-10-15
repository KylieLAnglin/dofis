
# # Convert strings to numeric
num_cols = ['teachers_nodegree_num', 'teachers_badegree_num', 'teachers_msdegree_num', 'teachers_phddegree_num',
    'teachers_num', 'teachers_exp_ave',
    'teachers_tenure_ave', 'stu_teach_ratio']
data[num_cols] = data[num_cols].apply(pd.to_numeric, errors='coerce')

# # Create variables


# Student characteristics

data['students_frpl'] = data['students_frpl_num'] / data['students_num']
data['students_black'] = data['students_black_num'] / data['students_num']
data['students_hisp'] = data['students_hisp_num'] / data['students_num']
data['students_white'] = data['students_white_num'] / data['students_num']

data['students_teacher_ratio'] = data['students_num'] / data['teachers_num']

# Performance

# Standardize within subject using mean and standard deviation from 2014-15
data = clean_for_merge.standardize_scores(data=data, std_year=2015)
elem_math = ['m_3rd_std', 'm_4th_std', 'm_5th_std']
elem_reading =  ['r_3rd_std', 'r_4th_std', 'r_5th_std']
elem = ['m_3rd_std', 'm_4th_std', 'm_5th_std','r_3rd_std', 'r_4th_std', 'r_5th_std']
sec_math = ['m_6th_std', 'm_7th_std', 'm_8th_std', 'alg_std']
sec_reading = ['r_6th_std', 'r_7th_std', 'r_8th_std',  'eng1_std']
sec_science = ['s_8th_std', 'bio_std']

all_scores = ['m_3rd_std', 'm_4th_std', 'm_5th_std', 'm_6th_std', 'm_7th_std', 'm_8th_std',
        'r_3rd_std', 'r_4th_std', 'r_5th_std', 'r_6th_std', 'r_7th_std', 'r_8th_std',
        's_8th_std',
        'alg_std', 'bio_std']

data['elem_math'] = data[elem_math].mean(axis=1)
data['elem_reading'] = data[elem_reading].mean(axis=1)
data['elem'] = data[elem].mean(axis=1)

data['sec_math'] = data[sec_math].mean(axis=1)
data['sec_reading'] = data[sec_reading].mean(axis = 1)
data['sec_science'] = data[sec_science].mean(axis = 1)
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
# Add charter geography based on geography of traditional public schools and FRPL
cnty_type = {}
for cnty in list(data['cntyname_c'].unique()):
geo_list = list(data[data.cntyname_c == cnty]['geography'].value_counts().keys())
try:
max_geo = geo_list[0]
cnty_type[cnty] = max_geo
except:
print(cnty)
print(geo_list)
new_geo = []
for geo, cnty, charter, frpl in zip(data.geography, data.cntyname_c, data.charter, data.students_frpl):
if charter == True:
if (frpl > .35) and (cnty_type[cnty] == 'Suburban'):
    new_geo.append('Urban')
else:
    new_geo.append(cnty_type[cnty])
else:
new_geo.append(geo)
data['geography'] = new_geo

# Geography indicators
data['type_urban'] = np.where(data['geography'] == 'Urban', 1, 0)
data['type_suburban'] = np.where(data['geography'] == 'Suburban', 1, 0)
data['type_town'] = np.where(data['geography'] == 'Town', 1, 0)
data['type_rural'] = np.where(data['geography'] == 'Rural', 1, 0)

data['eligible'] = np.where((data.distischarter == 'Y') | (data.rating_academic == 'F') |(data.rating_financial == 'Fail'), 0, 1)

# Always eligible?
#df_filter = data[['distname', 'year', 'eligible']]
#df_filter = df_filter[~df_filter['year'].isin(['yr1112', 'yr1213', 'yr1314'])]
#always_eligible = pd.DataFrame(df_filter.groupby(['distname'])['eligible'].min()).reset_index()
#always_eligible.columns = ['distname', 'always_eligible']
#data = data.merge(always_eligible.reset_index(), left_on='distname', right_on='distname', how='left')

#  Teacher Characteristics
data['teachers_nodegree'] = data['teachers_nodegree_num'] / data['teachers_num']
data['teachers_badegree'] = data['teachers_badegree_num'] / data['teachers_num']
data['teachers_msdegree'] = data['teachers_msdegree_num'] / data['teachers_num']
data['teachers_phddegree'] = data['teachers_phddegree_num'] / data['teachers_num']

# # Save
data.to_csv(os.path.join(start.data_path, 'clean', 'master_data.csv'),
    sep=",")

# GDID
#data = data[data.always_eligible == True]
#data = data[data.distischarter == "N"]
cols = [c for c in data.columns if c.lower()[:3] != 'reg']
data = data[cols]
data['doi_year'] = np.where((data.doi_year == 2015), np.nan, data.doi_year) #drop first implementer (one district)
data['treatpost'] = np.where(((data.year > data.doi_year) &(data.doi == True)), True, False)
data.to_csv(os.path.join(start.data_path, 'clean', 'gdid.csv'), sep=",")
