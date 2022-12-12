import os
import json
from datetime import datetime

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd


def init(filepath: str, vendor: str, description='', extension='csv'):
    # Read file
    df = pd.read_csv(filepath)

    # Get filename information
    dt = datetime.today().strftime('%Y%m%d%H%M')
    num_item = len(df.index)

    # Create filename
    filename = f'{dt}-{num_item}-{vendor}' + ('-' if description else '') + description

    # Create new files
    df.to_csv(f'data/input/{filename}.{extension}', index=False)

    # Init process key = 0
    with open('data/process.json', 'r') as f:
        process = json.load(f)

    process[filename] = 0

    with open('data/process.json', 'w') as f:
        json.dump(process, f)


def get_remaining(filename, column, extension='csv'):
    # Get current row
    with open('data/process.json', 'r') as f:
        process = json.load(f)

    if filename in process.keys():
        crow = process[filename]
    else:
        raise ValueError('Filename hasn\'t been initialized')

    # Read file
    df = pd.read_csv(f'data/input/{filename}.{extension}')

    return df[crow:][column].to_list()


def process(filename, info, success, extension='csv'):
    # Check process key
    with open('data/process.json', 'r') as f:
        process = json.load(f)

    v = process[filename]

    # Add info to correct file
    if success:
        if os.path.isfile(f'data/sresult/{filename}.{extension}'):
            df = pd.read_csv(f'data/sresult/{filename}.{extension}')
            df = df.append(info, ignore_index=True)
        else:
            df = pd.DataFrame(info, index=[0])

        df.to_csv(f'data/sresult/{filename}.{extension}', index=False)
    else:
        if os.path.isfile(f'data/uresult/{filename}.{extension}'):
            df = pd.read_csv(f'data/uresult/{filename}.{extension}')
            df = df.append(info, ignore_index=True)
        else:
            df = pd.DataFrame(info, index=[0])

        df.to_csv(f'data/uresult/{filename}.{extension}', index=False)

    # Increase value of process variable
    process[filename] += 1

    with open('data/process.json', 'w') as f:
        json.dump(process, f)


def clean(filename, extension='csv'):
    # Read file
    df = pd.read_csv(f'data/input/{filename}.{extension}')

    # Drop all rows from df
    df.drop(df.index, inplace=True)

    # Remove process files
    os.remove(f'data/sresult/{filename}.{extension}')
    os.remove(f'data/uresult/{filename}.{extension}')

    # Replace process key = 0
    with open('data/process.json', 'r') as f:
        process = json.load(f)

    process[filename] = 0

    with open('data/process.json', 'w') as f:
        json.dump(process, f)
