import datetime as dt

from functions.update_ticker_data_db import update_ticker_data_db

if __name__ == '__main__':
    end = dt.date.today()
    update_ticker_data_db(end)
