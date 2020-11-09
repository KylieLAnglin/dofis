import os
import fnmatch
import pandas as pd


def concat_files(path: str, pattern: str):
    """Search for all files matching pattern and concatenate

    Args:
        path (str): path to folder containing files of interest
        pattern (str): unix filename pattern with shell-style wildcards

    Returns:
        [pd.DataFrame]: dataframe of all concetenated files
    """
# Files
    files = []
    for entry in os.listdir(path):
        if fnmatch.fnmatch(entry, pattern):
            files.append(entry)
    files.sort()
    dirs_cert = [path + '/' + file for file in files]
    df_list = [pd.read_csv(file, sep=",", encoding="ISO-8859-1", dtype=object) for file in dirs_cert]
    df = pd.concat(df_list)

    return df

