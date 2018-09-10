import pandas as pd
import os
import shutil
import start


def filter_and_rename_cols(df, dict):
    """
    Keep some original cols from a dataframe, rename them to new column names
    Return a new dataframe

    Arguments:
    df = datarame
    dict keys = original column names you want to keep
    dict values = new column names
    """
    df = df[list(dict.keys())]
    new_df = df.rename(index=str, columns=dict)
    return new_df

def fix_parser_error(input_path):
    temp_directory = os.path.join(start.data_path, 'temp')
    temp_file = os.path.basename(input_path)
    temp_path = os.path.join(temp_directory, temp_file)

    print('Got a parser error - concatenating first two lines of text file to remedy!')
    shutil.copy(input_path, temp_path)
    input_path = temp_path
    print('Copied file to', input_path)

    with open(temp_path, 'r') as file:
        text_contents = file.read()
    text_contents = text_contents.replace('\n', '', 1)
    with open(temp_path, 'w') \
            as file:
        file.write(text_contents)
    print("Standardized!")
    return(temp_path)
