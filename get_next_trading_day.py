import datetime as dt
import time

from functions.get_elapsed import get_elapsed
from functions.resources import get_connection
from functions.trading_date import get_last_trading_date, get_next_trading_date


def main():
    con = get_connection()
    if con.open():
        day1 = 24 * 60 * 60

        # end: int = get_last_trading_date() - day1 * 14
        end: int = get_last_trading_date()
        con.close()

        day_last = dt.datetime.fromtimestamp(end)
        weekday = day_last.weekday()
        print('last day =', end, day_last, weekday)

        end_next = get_next_trading_date(end)
        day_next = dt.datetime.fromtimestamp(end_next)
        print('next day =', end_next, day_next, day_next.weekday())
    else:
        print('fail to open db.')


if __name__ == "__main__":
    time_start = time.time()
    main()
    print('elapsed %.3f sec' % get_elapsed(time_start))
