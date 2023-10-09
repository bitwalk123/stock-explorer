import datetime as dt
import os
import pickle
import time

from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dataset import get_valid_list_id_code


def main():
    """Simulate prediction performance using past data
    """
    # Constants
    count_min = 200
    volume_min = 10000

    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    day = 24 * 60 * 60
    year = 365 * day

    end_str = '2023-01-04'
    end_dt = dt.datetime.strptime(end_str, '%Y-%m-%d')

    # Loop condition
    duration = 250 * day
    origin = end = int(dt.datetime.timestamp(end_dt)) + tz_delta

    start = end - year
    print()
    print(conv_timestamp2date(start), conv_timestamp2date(end))
    end_next = 0

    # List valid id_code
    time_start = time.time()
    pkl_list_id_code = 'pool/list_id_code_%d.pkl' % end

    # List valid id_code
    time_start = time.time()
    if not os.path.isdir('pool'):
        os.mkdir('pool')
    pkl_list_id_code = 'pool/list_id_code_%d.pkl' % end

    # TODO:
    # Need to change split criteria.
    list_id_code = get_valid_list_id_code(start, end, count_min, volume_min)
    print(list_id_code)


if __name__ == "__main__":
    main()
