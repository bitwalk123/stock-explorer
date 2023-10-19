import datetime as dt

from functions.update_db import update_ticker

if __name__ == '__main__':
    end = dt.date.today()
    update_ticker(end)
