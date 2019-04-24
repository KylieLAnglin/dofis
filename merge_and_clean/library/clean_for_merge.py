import pandas as pd
import unicodedata

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
                        "HIGHLAND PARK ISD (057911)": "HIGHLAND PARK ISD (07911)",
                        "EDGEWOOD ISD (015905)": "EDGEWOOD ISD (15905)",
                        "HIGHLAND PARK ISD (07911)": "HIGHLAND PARK ISD (57911)",
                        "CULBERSON COUNTY-ALLAMOORE ISD": "CULBERSON COUNTY ALLAMOORE ISD"}
    df[col_name] = df[col_name].replace(fix_names)
    return df

def add_distnum_to_plan(df, col_name):
    fix_names = {"VALLEY VIEW ISD": "VALLEY VIEW ISD (49903)",
                 "DAWSON ISD": 'DAWSON ISD (58902)',
                 "BIG SANDY ISD": "BIG SANDY ISD (187901)",
                 "RICE ISD": "RICE ISD (45903)",
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


