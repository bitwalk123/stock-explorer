import datetime as dt
import time

from functions.get_elapsed import get_elapsed
from functions.update_db import (
    update_prediction,
    update_ticker,
)

if __name__ == '__main__':
    time_start = time.time()
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    end = dt.date.today()
    update_ticker(end)
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    update_prediction()
    print('elapsed %.3f sec' % get_elapsed(time_start))
