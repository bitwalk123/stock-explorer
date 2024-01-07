import datetime as dt
import pandas as pd
import time
import yfinance as yf

from PySide6.QtSql import QSqlQuery

from funcs.tbl_currency import get_dict_currency
from funcs.tbl_exchange import add_rows_tbl_exchange
from funcs.tide import get_elapsed, conv_timestamp2date_next, get_original_start
from snippets.set_env import set_env
from sqls.sql_exchange import sql_sel_max_date_from_exchange_with_id_currency
from structs.db_info import DBInfo


def update_tbl_exchange(end: dt.date) -> bool:
    # get dictionary of code with id_code as key
    dict_currency = get_dict_currency()

    con = DBInfo.get_connection()
    if con.open():
        for id_currency in dict_currency:
            currency = '%s=X' % dict_currency[id_currency]
            print(currency)
            # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
            # get latest date of the exchange table with specified id_currency
            query = QSqlQuery()
            sql = sql_sel_max_date_from_exchange_with_id_currency(id_currency)
            query.exec(sql)
            while query.next():
                date_latest = query.value(0)
                if type(date_latest) is int:
                    start = conv_timestamp2date_next(date_latest)
                else:
                    start = get_original_start()
                if start == end:
                    print('Skipped due to start and end are the same!')
                    continue
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # get data from Yahoo finance
                df: pd.DataFrame = yf.download(currency, start, end)
                size_row = len(df)
                if size_row == 0:
                    print('Skipped due to no data is obtained!')
                    continue
                print('data size: %d.' % size_row)
                add_rows_tbl_exchange(df, id_currency)
        con.close()
        return True
    else:
        print('database can not be opened!')
        return False

if __name__ == '__main__':
    dict_info = set_env()
    time_start = time.time()
    end = dt.date.today()
    result = update_tbl_exchange(end)
    print(result)
    print('elapsed %.3f sec' % get_elapsed(time_start))
