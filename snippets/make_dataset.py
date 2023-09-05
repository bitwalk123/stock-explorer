import datetime as dt
import os
import time

import pandas as pd

from functions.get_dataset import get_valid_list_id_code
from functions.get_elapsed import get_elapsed


def main():
    """Main
    """
    time_start = time.time()
    today = int(pd.to_datetime(str(dt.date.today())).timestamp())
    year = 365 * 24 * 60 * 60
    start = today - year
    print(start)
    count_min = 200
    volume_min = 10000

    list_id_code = get_valid_list_id_code(start, count_min, volume_min)
    print('total :', len(list_id_code))
    print('elapsed', get_elapsed(time_start), 'sec')


if __name__ == "__main__":
    os.chdir('../')
    main()
