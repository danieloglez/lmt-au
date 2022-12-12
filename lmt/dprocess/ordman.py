import glob
import json
import pandas as pd

DIRTY_DIR = 'data/order/dirty'
CLEAN_DIR = 'data/order/clean'
PROCESS_PATH = 'data/order/process.json'


def switch_days():
    # Read process json
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    # Extract new filename
    new_filename = sorted(glob.glob('data/dirty/*'))[-1].split('/')[-1].replace('.csv', '')

    order = process['order']
    order.append(new_filename)
    process['order'] = list(set(order))

    # Save process json
    with open(PROCESS_PATH, 'w') as f:
        json.dump(process, f)


def clean_current_orders(extension='csv'):
    # Read process json
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    # Extract filenames
    p_filename = process["order"][-2]
    c_filename = process["order"][-1]

    # Read dataframes
    l_df = pd.read_csv(f'{DIRTY_DIR}/{p_filename}.{extension}')
    c_df = pd.read_csv(f'{DIRTY_DIR}/{c_filename}.{extension}')

    # Execute outer join for only c_df elements
    r_df = l_df.merge(c_df, on='Store Order ID', how='outer', indicator=True)
    r_df = r_df[r_df['_merge'] == 'right_only'].drop('_merge', 1)

    # Delete columns from left dataframe and remove postfixes
    del_cols = [col for col in r_df.keys().tolist() if '_x' in col]

    for col in del_cols:
        del r_df[col]

    for col in r_df.keys().tolist():
        r_df.rename(columns={col: col.replace('_y', '')}, inplace=True)

    # Change types
    r_df = r_df.astype({'Sales': str, 'QTY': int})
    r_df['Sales'] = [i.replace('.0', '') for i in r_df['Sales']]

    # Save csv
    r_df.to_excel(f'{CLEAN_DIR}/{c_filename}.xlsx', index=False)
