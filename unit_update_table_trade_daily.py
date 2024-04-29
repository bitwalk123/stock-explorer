import datetime as dt
import time

from PySide6.QtWidgets import QApplication

from funcs.tbl_trade import update_tbl_trade
from funcs.tide import get_elapsed
from snippets.set_env import set_env

if __name__ == '__main__':
    dict_info = set_env()
    time_start = time.time()
    end = dt.date.today()
    result = update_tbl_trade(end)
    print(result)
    print('elapsed %.3f sec' % get_elapsed(time_start))
