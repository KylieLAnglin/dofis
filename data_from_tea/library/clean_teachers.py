import pandas as pd

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
                  'Temporary Exemption': True, 'Temporary Teaching Certificate': False,
                  'Unknown Permit': False, 'Unknown': False,
                  'Special Assignment': True,
                  'Paraprofessional': False, 'Standard Paraprofessional': False, 'Non-renewable': False,
                  'Standard': True, 'Provisional': True,
                  'Probationary': True, 'Probationary Extension': True, 'Probationary Second Extension': True,
                  'One Year': True,
                  'Visiting International Teacher': True,
                  'Professional': True, 'Standard Professional': True}
    cert['certified'] = cert['cert_type'].map(cert_types)

    return cert
