import gc
import pandas as pd
from lmt.suredone import api
from lmt.dprocess import ordman


if __name__ == '__main__':
    # Extract awaiting orders and saves them in data/dirty/
    orders = api.get_awaiting_orders()

    # Adds the new file in process.json
    ordman.switch_days()

    # Keep new records only
    ordman.clean_current_orders()