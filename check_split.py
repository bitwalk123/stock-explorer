import datetime as dt
import sys

from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_date_open_from_trade_with_id_code_start_end,
)
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dict_code import get_dict_code
from functions.resources import get_connection


class preProcess():
    factor_split = 1.5

    def __init__(self, id_code: int, start:int, end:int):
        self.id_code = id_code
        self.start = start
        self.end = end
        self.date = 0
        self.price_open = 0
        self.price_open_pre = -1

    def is_split(self) -> bool:
        flag_date = self.price_open_pre > 0
        flag_upper = self.price_open_pre / self.factor_split > self.price_open
        flag_lower = self.price_open_pre * self.factor_split < self.price_open
        return flag_date and (flag_upper or flag_lower)

    def check(self) -> bool:
        sql = get_sql_select_date_open_from_trade_with_id_code_start_end(
            self.id_code, self.start, self.end
        )
        query = QSqlQuery(sql)
        while query.next():
            self.date = query.value(0)
            self.price_open = query.value(1)
            if self.is_split():
                return True
            self.price_open_pre = self.price_open

        return False


def main():
    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone

    start_str = '2022-01-04'
    start_dt = dt.datetime.strptime(start_str, '%Y-%m-%d')
    start = int(dt.datetime.timestamp(start_dt)) + tz_delta
    end_dt = dt.datetime.now()
    end = int(dt.datetime.timestamp(end_dt)) + tz_delta
    print(start, conv_timestamp2date(start), '-', end, conv_timestamp2date(end))

    num_total = 0
    con = get_connection()
    if con.open():
        print('success to open db.')
        # prepare dictionary for id_code and code
        dict_code: dict = get_dict_code()

        for id_code in dict_code.keys():
            code = dict_code[id_code]
            checker = preProcess(id_code, start, end)
            if checker.check():
                num_total += 1
                print(
                    '%d.T' % code,
                    conv_timestamp2date(checker.date),
                    checker.price_open_pre, '>>',
                    checker.price_open, ':',
                    checker.price_open - checker.price_open_pre
                )

        con.close()
    else:
        print('fail to open db.')

    print('total', num_total)


if __name__ == "__main__":
    main()
