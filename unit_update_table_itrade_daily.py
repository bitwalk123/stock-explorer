import datetime as dt
import time

from funcs.tbl_itrade import update_tbl_itrade
from funcs.tide import get_elapsed
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()
    time_start = time.time()
    end = dt.date.today()
    result = update_tbl_itrade(end)
    print(result)
    print('elapsed %.3f sec' % get_elapsed(time_start))
