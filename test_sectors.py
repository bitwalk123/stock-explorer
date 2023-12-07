from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import select_13sector_from_ticker_with_code, select_13sector_from_ticker
from database.sqls_trade import select_close_from_trade_with_id_code_date
from functions.get_dict_code import get_dict_code_id_code
from functions.get_latest_2dates import get_latest_2dates
from functions.resources import get_connection


def compare_close(pair_date):
    dict_plus = dict()
    dict_minus = dict()
    dict_zero = dict()
    con = get_connection()
    if con.open():
        # dictionary for id_code with key of code
        dict_id_code = get_dict_code_id_code()
        # _____________________________________________________________________
        # Initialize dictionary for 33業種区分
        set_13sector = set()
        sql = select_13sector_from_ticker()
        query = QSqlQuery(sql)
        while query.next():
            set_13sector.add(query.value(0))
        list_13sector = list(sorted(set_13sector))
        for sector in list_13sector:
            dict_plus[sector] = 0
            dict_minus[sector] = 0
            dict_zero[sector] = 0
        for code in dict_id_code.keys():
            # _________________________________________________________________
            # 33業種区分
            name_13sector = ''
            sql = select_13sector_from_ticker_with_code(code)
            query = QSqlQuery(sql)
            if query.next():
                name_13sector = query.value(0)
            # _________________________________________________________________
            # day 1
            sql = select_close_from_trade_with_id_code_date(
                dict_id_code[code], pair_date[0]
            )
            query = QSqlQuery(sql)
            if query.next():
                close_1 = query.value(0)
            else:
                close_1 = 0
            if close_1 == 0:
                continue
            # _________________________________________________________________
            # day 2
            sql = select_close_from_trade_with_id_code_date(
                dict_id_code[code], pair_date[1]
            )
            query = QSqlQuery(sql)
            if query.next():
                close_2 = query.value(0)
            else:
                close_2 = 0
            if close_2 == 0:
                continue

            diff = close_2 - close_1
            if diff > 0:
                dict_plus[name_13sector] += 1
            elif diff < 0:
                dict_minus[name_13sector] += 1
            else:
                dict_zero[name_13sector] += 1

        con.close()
        print(dict_plus)
        print(dict_minus)
        print(dict_zero)


if __name__ == '__main__':
    pair_date = get_latest_2dates()
    print(pair_date)
    compare_close(pair_date)
