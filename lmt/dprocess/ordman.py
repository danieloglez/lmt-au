import glob
import json
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime


DIRTY_DIR = 'data/order/dirty'
CLEAN_DIR = 'data/order/clean'
PROCESS_PATH = 'data/order/process.json'


# def switch_days():
#     # Read process json
#     with open(PROCESS_PATH, 'r') as f:
#         process = json.load(f)
#
#     # Extract new filename
#     new_filename = glob.glob(f'{DIRTY_DIR}/*')[-1].split('/')[-1].replace('.csv', '')
#
#     # Set new current if different
#     if new_filename != process['current']:
#         process['previous'] = process['current']
#         process['current'] = new_filename
#
#     # Save process json
#     with open(PROCESS_PATH, 'w') as f:
#         json.dump(process, f)


def clean_current_orders(extension='csv'):
    # Read process json
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    # Extract filenames
    p_filename = process['previous']
    c_filename = process["current"]

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

def send_email(fromaddr, toaddr):
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = f"Orders from {datetime.today().strftime('%Y-%m-%d')}"

    # string to store the body of the mail
    body = "See attachment"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # read process json
    with open(PROCESS_PATH, 'r') as f:
        process = json.load(f)

    # open the file to be sent
    filename = f'{process["current"]}.xlsx'
    attachment = open(f'{CLEAN_DIR}/{filename}', "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.outlook.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "danID_06367")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()