import datetime as dt
import time

from PySide6.QtSql import QSqlQuery

from functions.get_elapsed import get_elapsed
from functions.update_db import update_ticker

if __name__ == '__main__':
    time_start = time.time()
    end = dt.date.today()
    queries = [QSqlQuery() for k in range(4)]
    update_ticker(end, queries)
    print('elapsed %.3f sec' % get_elapsed(time_start))
