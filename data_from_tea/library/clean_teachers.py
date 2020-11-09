import pandas as pd
import numpy as np

from dofis.data_from_tea.library import start


def clean_grades(df: pd.DataFrame, col: str):
    """Replace grade values so they're numeric

    Args:
        df (pd.DataFrame): [description]
        col (str): [description]
    """
    df[col] = df[col].replace({'Grades ': ''}, regex=True)
    grades = {'12-Aug': '8-12', '12-Jul': '7-12',
              '12-Jun': '6-12', '6-Jan': '1-6',
              '8-Apr': '4-8', '8-Jan': '1-8', 'EC-12': '0-12',
              'EC-4': '0-4', 'EC-6': '0-6', 'PK-12': '0-12',
              'PK-3': '0-3', 'PK-6': '0-6', 'PK-KG': '0-1'}
    df[col] = df[col].replace(grades)

    return df


def split_grades(df: pd.DataFrame, col: str,
                 low_name: str, high_name: str):
    """split grade columnm into low and high grades

    Args:
        df (pd.DataFrame): dataframe containing grade column
        col (str): column containing grades separated by hyphen
        low_name (str): new column name with low grade
        high_name (str): new column name with high grade

    """

    df[low_name], df[high_name] = df[col].str.split(
        '-').str
    df[low_name] = pd.to_numeric(df[low_name], errors='coerce')
    df[high_name] = pd.to_numeric(df[high_name], errors='coerce')

    return df


def define_certification():
    # Create certification variable
    cert_types = {'Emergency Non-Certified': False,
                  'Emergency Certified': True,
                  'Emergency': False, 'Emergency Teaching': False,
                  'Temporary Exemption': True,
                  'Temporary Teaching Certificate': False,
                  'Unknown Permit': False, 'Unknown': False,
                  'Special Assignment': True,
                  'Paraprofessional': False,
                  'Standard Paraprofessional': False, 'Non-renewable': False,
                  'Standard': True, 'Provisional': True,
                  'Probationary': True, 
                  'Probationary Extension': True,
                  'Probationary Second Extension': True,
                  'One Year': True,
                  'Visiting International Teacher': True,
                  'Professional': True, 'Standard Professional': True}
    cert['certified'] = cert['cert_type'].map(cert_types)

    return cert


def gen_standard_certification(df: pd.DataFrame, col: str, new_var: str):
    """Generate binary variable for whether a certification
    is standard - here defined as a certification completed or
    in progress through State Board for Educator Certification

    Args:
        df (pd.DataFrame): dataset containing CREDENITAL_TYPE
        col (str): Column containing TEA defn'd credential types
        new_var (str): Name of new variable containing certification 
            category

    Three types: Stanr
    """
    cert_dict = {'Emergency Non-Certified': 0,
                 'Emergency Certified': 0,
                 'Emergency': 0,
                 'Emergency Teaching': 0,
                 'Temporary Exemption': 0,
                 'Temporary Teaching Certificate': 0,
                 'Unknown Permit': 0, 'Unknown': 0,
                 'Special Assignment': 0,
                 'Non-renewable': 0,
                 'Standard': 1,
                 'Provisional': 1,
                 'Probationary': 1,
                 'Probationary Extension': 1,
                 'Probationary Second Extension': 1,
                 'One Year': 1,
                 'Visiting International Teacher': 0,
                 'Professional': 1,
                 'Standard Professional': 1,
                 'Vocational': 0}

    df[new_var] = df[col].map(cert_dict)

    return df


def gen_subject(df: pd.DataFrame, new_col: str,
                area_tuple: tuple,
                level_tuple: tuple = (),
                standard_tuple: tuple = ()):
    """[summary]

    Args:
        df (pd.DataFrame): input and output data
        new_col (str): New column name
        area_tuple (tuple): tuple with TEA cert area column and value
        level_tuple (tuple, optional): tuple with TEA cert level columna and value. Defaults to {}.
        standard_tuple (tuple, optional): tuple with standard cert bool col and value. Defaults to {}.
    """

    df[new_col] = np.where(df[area_tuple[0]] == area_tuple[1], True, False)

    if len(level_tuple) > 0:
        df[new_col] = np.where(df[level_tuple[0]] == level_tuple[1],
                               df[new_col],
                               False)

    if len(standard_tuple) > 0:
        df[new_col] = np.where(df[standard_tuple[0]] == standard_tuple[1],
                               df[new_col],
                               False)

    return df


