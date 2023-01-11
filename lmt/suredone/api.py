import math
import requests
import json
import pandas as pd
from tqdm import tqdm
from datetime import datetime


DIRTY_DIR = 'data/order/dirty'
PROCESS_PATH = 'data/order/process.json'

E_AWAITING = 'https://api.suredone.com/v1/orders/awaiting'

HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Auth-User': 'feles99',
    'X-Auth-Token': '4160D2FE416CF3E2DD5C245A03DCDB39A2DB17662F662EFDAC09B511EDB73F3F6946AED63F737D7617JUBMJJH5XAOM5HILFG0P6QQ1RAM1'
}

FIELD_MAP = {
    'order': 'Store Order ID',
    'sales': 'Sales',
    'receive': 'RECIEVE (Yes or Blank)',
    'qtys': 'QTY',
    'orderingpn': 'Ordering PN',
    'manufacturerpartnumber': 'Manufacturer PN',
    'title': 'Description',
    'cost': 'SD Cost',
    'price': 'SD Price',
    'date': 'Order Date',
    'paymenttime': 'Paid Date',
    'receiveddate': 'Received Date',
    'vendor': 'Vendor',
    'orderingpn2': 'Ordering PN2',
    'locationinwarehouse': 'Warehouse Location',
    'invoicenumber': 'Invoice #',
    'notas': 'NOTAS',
    'warehouse': 'WAREHOUSE',
    'bigcommerceprice': 'bigcommerceprice',
    'amznprice': 'amznprice',
    'walmartprice': 'walmartprice',
    'ebayid': 'ebayid',
    'inventorydate': 'inventorydate'
}


def n_pages():
    return math.ceil(float(requests.get(E_AWAITING, headers=HEADERS).json()['all']) / 50) + 1


def get_awaiting_orders():
    # Create empty dict
    orders_dict = {}

    for v in FIELD_MAP.values():
        orders_dict[v] = []

    n = n_pages()

    for i in tqdm(range(1, n)):
        process_orders_page(requests.get(
            f'{E_AWAITING}?page={i}', headers=HEADERS).json(), orders_dict)

    # Create new_filename
    filename = datetime.today().strftime("%Y%m%d")
    # filename = '20230109-TEST'

    # Read process json
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    # Set new current if different
    if filename != process['current']:
        process['previous'] = process['current']
        process['current'] = filename

    # Save process json
    with open(PROCESS_PATH, 'w') as f:
        json.dump(process, f)

    df = pd.DataFrame(orders_dict)
    df.to_csv(f'{DIRTY_DIR}/{filename}.csv', index=False)


def process_orders_page(orders_page, orders_dict):
    # Delete unnecessary fields
    del orders_page['all']
    del orders_page['time']

    for k in orders_page.keys():
        for item_key in orders_page[k]['item'].keys():
            process_order(orders_page[k], item_key, orders_dict)


def process_order(order, item_key, orders_dict):
    # Append first level coincidences
    for k in order.keys():
        if k in FIELD_MAP.keys():
            if k == 'qtys':
                orders_dict[FIELD_MAP[k]].append(order[k].split('*')[int(item_key)])
            else:
                orders_dict[FIELD_MAP[k]].append(order[k])

    # Append 2nd level coincidences
    item_dict = order['item'][item_key]

    for k in item_dict.keys():
        if k in FIELD_MAP.keys():
            orders_dict[FIELD_MAP[k]].append(item_dict[k])

    # Append rest of fields
    r_sales = order['order']

    if 'bigcommerce' in r_sales or 'walmart' in r_sales:
        r_sales = r_sales.replace('bigcommerce', '').replace('walmart', '')
    else:
        r_sales = r_sales.split('-')[-1]

    orders_dict['Sales'].append(r_sales)
    orders_dict['RECIEVE (Yes or Blank)'].append('')
    orders_dict['Received Date'].append('')
    orders_dict['Invoice #'].append('')
    orders_dict['NOTAS'].append('')
    orders_dict['WAREHOUSE'].append('')

    # Fill gaps
    m = max([len(v) for k, v in orders_dict.items()])

    for arr in orders_dict.values():
        if len(arr) < m:
            arr.append('')
