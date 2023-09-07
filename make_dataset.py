import datetime as dt
import os
import pickle
import time

import pandas as pd

from functions.get_dataset import get_valid_list_id_code, get_target_list_id_code
from functions.get_elapsed import get_elapsed


def main():
    """Main
    """
    today = int(pd.to_datetime(str(dt.date.today())).timestamp())
    year = 365 * 24 * 60 * 60
    start = today - year
    print(start)
    count_min = 200
    volume_min = 10000
    price_min = 500
    price_max = 600

    # List valid id_code
    time_start = time.time()
    pkl_list_id_code = 'pool/list_id_code.pkl'
    if os.path.isfile(pkl_list_id_code):
        with open(pkl_list_id_code, 'rb') as f:
            list_id_code = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        list_id_code = get_valid_list_id_code(start, count_min, volume_min)
        with open(pkl_list_id_code, 'wb') as f:
            pickle.dump(list_id_code, f)

    print('total :', len(list_id_code))
    print('elapsed', get_elapsed(time_start), 'sec')

    # pick target id_code
    time_start = time.time()
    list_id_code_target = get_target_list_id_code(list_id_code, price_min, price_max)

    print('total :', len(list_id_code_target))
    print('elapsed', get_elapsed(time_start), 'sec')

if __name__ == "__main__":
    main()
