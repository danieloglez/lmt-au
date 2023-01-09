import os
import json
from datetime import datetime

import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd


INPUT_DIR = 'data/scrap/input'
SRESULT_DIR = 'data/scrap/sresult'
URESULT_DIR = 'data/scrap/uresult'
PROCESS_PATH = 'data/scrap/process.json'


def init(filepath: str, vendor: str, description='', extension='csv'):
    # Read file
    df = pd.read_csv(filepath)

    # Get filename information
    dt = datetime.today().strftime('%Y%m%d%H%M')
    num_item = len(df.index)

    # Create filename
    filename = f'{dt}-{num_item}-{vendor}' + ('-' if description else '') + description

    # Create new files
    df.to_csv(f'{INPUT_DIR}/{filename}.{extension}', index=False)

    # Init process key = 0
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    process[filename] = 0

    with open(PROCESS_PATH, 'w') as f:
        json.dump(process, f)


def get_remaining(filename, extension='csv'):
    # Get current row
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    if filename in process.keys():
        crow = process[filename]
    else:
        raise ValueError('Filename hasn\'t been initialized')

    # Read file
    df = pd.read_csv(f'{INPUT_DIR}/{filename}.{extension}')

    return df[crow:]


def process(filename, info, additional, success, extension='csv'):
    # Check process key
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    v = process[filename]

    for k, v in additional.items():
        info[k] = v

    # Add info to correct file
    if success:
        if os.path.isfile(f'{SRESULT_DIR}/{filename}.{extension}'):
            df = pd.read_csv(f'{SRESULT_DIR}/{filename}.{extension}')
            df = df.append(info, ignore_index=True)
        else:
            df = pd.DataFrame(info, index=[0])

        df.to_csv(f'{SRESULT_DIR}/{filename}.{extension}', index=False)
    else:
        if os.path.isfile(f'{URESULT_DIR}/{filename}.{extension}'):
            df = pd.read_csv(f'{URESULT_DIR}/{filename}.{extension}')
            df = df.append(info, ignore_index=True)
        else:
            df = pd.DataFrame(info, index=[0])

        df.to_csv(f'{URESULT_DIR}/{filename}.{extension}', index=False)

    # Increase value of process variable
    process[filename] += 1

    with open(PROCESS_PATH, 'w') as f:
        json.dump(process, f)


def clean(filename, extension='csv'):
    # Read file
    df = pd.read_csv(f'{INPUT_DIR}/{filename}.{extension}')

    # Drop all rows from df
    df.drop(df.index, inplace=True)

    # Remove process files
    os.remove(f'{SRESULT_DIR}/{filename}.{extension}')
    os.remove(f'{URESULT_DIR}/{filename}.{extension}')

    # Replace process key = 0
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    process[filename] = 0

    with open(PROCESS_PATH, 'w') as f:
        json.dump(process, f)
