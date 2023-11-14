import time

from functions.get_elapsed import get_elapsed
from functions.update_ticker_tbl import update_ticker_tbl

if __name__ == '__main__':
    time_start = time.time()
    update_ticker_tbl()
    elapsed = get_elapsed(time_start)
    print('finished updating! (%.3f sec)' % elapsed)

