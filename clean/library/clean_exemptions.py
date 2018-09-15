import pandas as pd
import unicodedata

def resolve_unicode_problems(df, col_name):
    """ Resolve Unicode problems from web scraping (e.g., 'Bronte\xa0ISD')"""
    df = df.copy()
    df[col_name] = df[col_name].map(lambda x: unicodedata.normalize('NFKD', x))
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
                         "WEST HARDIN COUNTY ISD": "WEST HARDIN ISD"}
    df[col_name] = df[col_name].replace(fix_names)
    return df

def distnum_in_paren(df, distname = 'distname', distnum = 'district'):
    df[distname] = (
            df[distname] +
            ' (' +
            df.pipe(lpad_nums, distnum, 6)[distnum].astype(str) +
            ')'
    )
    return df

def lpad_nums(df, col_name, length):
    """lpad the integer strings in a column to a set length"""
    df = df.copy()
    df[col_name] = df[col_name].astype(str).str.zfill(length)
    return df



