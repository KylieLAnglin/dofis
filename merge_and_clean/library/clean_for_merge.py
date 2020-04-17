import pandas as pd
import unicodedata
import os
from library import start

def resolve_unicode_problems(df, col_name):
    """ Resolve Unicode problems from web scraping (e.g., 'Bronte\xa0ISD')"""
    df = df.copy()
    df[col_name] = df[col_name].map(lambda x: unicodedata.normalize('NFKD', str(x)))
    return df

def uppercase_column(df, col_name):
    """Uppercase all the values in a column"""
    df = df.copy()
    df[col_name] = df[col_name].map(lambda x: x.upper())
    return df

def replace_column_values(df, col_name, string_to_replace, string_to_replace_with):
    """Run string replace on all values in a column"""
    df = df.copy()
    df[col_name] = df[col_name].str.replace(string_to_replace, string_to_replace_with).str.strip()
    return df

def sync_district_names(df, col_name):
    fix_names = {"EAGLE MT-SAGINAW ISD": "EAGLE MOUNTAIN SAGINAW ISD",
                         "FT SAM HOUSTON ISD": "FORT SAM HOUSTON ISD",
                         "GOLD BURG ISD": "GOLD-BURG ISD",
                         "KNOX CITY-O'BRIEN ISD": "KNOX CITY-O’BRIEN ISD",
                         "LEVERETTS CHAPEL ISD": "LEVERETT'S CHAPEL ISD",
                         "MARTINS MILL ISD": "MARTIN'S MILL ISD",
                         "MOUNT VERNON ISD": "MT. VERNON ISD",
                         "SAN FELIPE-DEL RIO ISD": "SAN FELIPE DEL RIO ISD",
                         "SCHERTZ-CIBOLO-U CITY ISD": "SCHERTZ-CIBOLO-UNIVERSAL CITY ISD",
                         "SCHLEICHER ISD": "SCHLEICHER COUNTY ISD",
                         "SPLENDORA ISD": "SPLENDORA ISD:",
                         "CARROLLTON-FARMERS BRANCH ISD": "CARROLLTON FARMERS BRANCH ISD",
                         "FT HANCOCK ISD": "FORT HANCOCK ISD",
                         "WEST HARDIN COUNTY ISD": "WEST HARDIN ISD",
                         "WEST HARDIN CISD": "WEST HARDIN ISD",
                        "WYLIE ISD (043914)": "WYLIE ISD (43914)",
                        "HUBBARD ISD (019913)": "HUBBARD ISD (19913)",
                        "EDGEWOOD ISD (015905)": "EDGEWOOD ISD (15905)",
                        "HIGHLAND PARK ISD (057911)": "HIGHLAND PARK ISD (57911)",
                        "HIGHLAND PARK ISD (07911)": "HIGHLAND PARK ISD (57911)",
                        "CULBERSON COUNTY-ALLAMOORE ISD": "CULBERSON COUNTY ALLAMOORE ISD",
                        }
    df[col_name] = df[col_name].replace(fix_names)
    return df

def add_distnum_to_plan(df, col_name):
    fix_names = {"VALLEY VIEW ISD": "VALLEY VIEW ISD (049903)",
                 "DAWSON ISD": 'DAWSON ISD (058902)',
                 "BIG SANDY ISD": "BIG SANDY ISD (187901)",
                 "RICE ISD": "RICE ISD (045903)",
                 "RICE CISD": "RICE ISD (175911)"}
    df[col_name] = df[col_name].replace(fix_names)
    return df



def distnum_in_paren(df, distname = 'distname', distnum = 'district'):
    df[distname] = (
            df[distname] +
            ' (' +
            df.pipe(lpad_nums, distnum, 6)[distnum].astype(str) + ')')
    return df

def lpad_nums(df, col_name, length):
    """lpad the integer strings in a column to a set length"""
    df = df.copy()
    df[col_name] = df[col_name].astype(str).str.zfill(length)
    return df

def strip_distnum_parens(str_list):
    new_list = [elem[0: -9] for elem in str_list]
    return new_list

def get_not_in(df_a, col_a, df_b, col_b):
    a_not_in_b = df_a[[elem not in list(df_b[col_b]) for elem in list(df_a[col_a])]]
    return a_not_in_b


def standardize_scores(data, std_year):
    yr_df = data[data.year == std_year]
    subjects = ['r_3rd', 'm_3rd', 'r_4th', 'm_4th', 'r_5th', 'm_5th',
                'r_6th', 'm_6th', 'r_7th', 'm_7th', 'r_8th', 'm_8th',
                's_8th',
                'alg', 'bio', 'eng1', 'eng2', 'us']
    means = []
    sds = []
    for var in subjects:
        sub = var + '_avescore'
        mean = yr_df[sub].mean()
        means.append(mean)
        sd = yr_df[sub].std()
        sds.append(sd)

    for sub, mean, sd in zip(subjects, means, sds):
        old_var = sub + "_avescore"
        new_var = sub + "_std"
        data[new_var] = (data[old_var] - mean) / sd

    return data


def merge_district_and_exemptions(tea_df, laws_df, geo_df):
    tea, laws = resolve_merge_errors(tea_df, laws_df)
    data = tea.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
    data.loc[(data['_merge'] == 'both'), 'doi'] = True
    data.loc[(data['_merge'] == 'left_only'), 'doi'] = False
    data = data.merge(geo_df, left_on='cntyname', right_on='county', how='left', indicator=False)
    print(laws.distname.nunique(), tea.distname.nunique(), data.distname.nunique())

    return data

def merge_school_and_exemptions(tea_df, laws_df, teacher_df, geo_df):
    tea, laws = resolve_merge_errors(tea_df, laws_df)
    data = tea.merge(laws, left_on='distname', right_on='distname', how='left', indicator=True)
    data.loc[(data['_merge'] == 'both'), 'doi'] = True
    data.loc[(data['_merge'] == 'left_only'), 'doi'] = False
    data = data.merge(teacher_df, left_on = ['campus', 'year'], right_on = ['campus', 'year'], how = 'left')
    data = data.merge(geo_df, left_on='cntyname', right_on='county', how='left', indicator=False)
    print(laws.distname.nunique(), tea.distname.nunique(), data.distname.nunique())
    print(tea.campus.nunique(), data.campus.nunique())

    return data

def import_tea_district():
    tea = pd.read_csv(os.path.join(start.data_path, 'tea', "desc_long.csv"),
            sep=",", low_memory = False)
    variables = ['year', 'district', 'distname', 'distischarter',
            'rating_academic', 'rating_financial',
            'type', 'type_description', 'cntyname']
    variables = variables + (list(tea.filter(regex = ("students"))))
    variables = variables + (list(tea.filter(regex = ("teachers"))))
    variables = variables + (list(tea.filter(regex = ("avescore"))))
    variables = variables + (list(tea.filter(regex = ("numtakers"))))
    variables = variables + (list(tea.filter(regex = ("days"))))
    variables = variables + (list(tea.filter(regex = ("class_size"))))
    variables = variables + ['stu_teach_ratio']
    tea = tea[variables]

    return tea

def import_tea_school():
    tea = pd.read_csv(os.path.join(start.data_path, 'tea', 'desc_c_long.csv'),
            sep=",", low_memory = False)
    variables = ['year', 'campus', 'campname', 'campischarter', 'district', 'distname', 'distischarter',
            'rating_academic', 'rating_financial','rating_academic_c',
            'type', 'type_description', 'cntyname']
    variables = variables + (list(tea.filter(regex = ("students"))))
    variables = variables + (list(tea.filter(regex = ("teachers"))))
    variables = variables + (list(tea.filter(regex = ("avescore"))))
    variables = variables + (list(tea.filter(regex = ("numtakers"))))
    variables = variables + (list(tea.filter(regex = ("days"))))
    variables = variables + (list(tea.filter(regex = ("class_size"))))
    variables = variables + ['stu_teach_ratio']
    tea = tea[variables]

    return tea
# Import TEA data and select columns

def import_laws():
    # Import DOI data and select columns
    laws = pd.read_csv(os.path.join(start.data_path, 'plans', 'doi_final.csv'),
                sep=",")
    cols = [c for c in laws.columns if c.lower()[:7] != 'Unnamed']
    laws = laws[cols]
    laws = laws.rename({'district': 'distname'}, axis=1)
    return laws

def import_geo():
    # Geographic data
    geo = pd.read_csv(os.path.join(start.data_path, 'geo', '2016_txpopest_county.csv'),
                sep=",")
    geo = geo[['county', 'july1_2016_pop_est']]
    geo = geo.rename({'july1_2016_pop_est': 'cnty_pop'}, axis='columns')
    geo['cnty_pop'] = geo['cnty_pop'] / 1000
    geo['cnty_pop'] = geo['cnty_pop'].round(0)
    geo = uppercase_column(geo, 'county')

    return geo

def import_teachers():
    teachers = pd.read_csv(os.path.join(start.data_path, 'tea', 'certification_rates_long.csv'),
            sep=",", low_memory = False)
    
    return teachers

def resolve_merge_errors(tea, laws):
    # problems with district name from scraping
    tea = tea.pipe(resolve_unicode_problems, 'distname')
    laws = laws.pipe(resolve_unicode_problems, 'distname')

    # scraped names in title case, but tea all caps. change scraped distname to caps
    laws = laws.pipe(uppercase_column, 'distname')

    # Add district numbers to some plans
    laws = add_distnum_to_plan(laws, 'distname')

    # sometimes districts named CISD othertimes ISD. Make all ISD
    tea = replace_column_values(tea, 'distname', 'CISD', 'ISD')
    laws = replace_column_values(laws, 'distname', 'CISD', 'ISD')

    # fix district names that don't match
    tea = sync_district_names(tea, 'distname')
    laws = sync_district_names(laws, 'distname')

    mismatch = get_not_in(laws, 'distname', tea, 'distname')
    mismatch_list = strip_distnum_parens(list(mismatch.distname))

    df = distnum_in_paren(
    tea[[elem in mismatch_list for elem in tea.distname]])

    tea.loc[(tea['distname'].isin(mismatch_list)), 'distname'] = (
    tea.loc[(tea['distname'].isin(mismatch_list))]
    .pipe(distnum_in_paren)['distname']
    )
    return tea, laws
