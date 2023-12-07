from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import (
    select_13sector_from_ticker,
    select_13sector_from_ticker_with_code,
)
from database.sqls_trade import select_close_from_trade_with_id_code_date
from functions.get_dict_code import get_dict_code_id_code
from functions.get_latest_2dates import get_latest_2dates
from functions.resources import get_connection
from structs.sector_delta import SectorDelta


def diff_close_by_sector(pair_date):
    dict_sector = dict()
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
            dict_sector[sector] = list()
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
            dict_sector[name_13sector].append(diff)

        con.close()
        sd = SectorDelta(dict_sector)
        for sector in sd.get_sectors():
            print(sector, sd.get_data(sector))


if __name__ == '__main__':
    pair_date = get_latest_2dates()
    print(pair_date)
    diff_close_by_sector(pair_date)
