import datetime as dt
import time

from functions.get_elapsed import get_elapsed
from functions.update_db import (
    update_prediction,
)

if __name__ == '__main__':
    time_start = time.time()
    end = dt.date.today()
    # update_ticker(end)
    update_prediction()
    print('elapsed %.3f sec' % get_elapsed(time_start))
