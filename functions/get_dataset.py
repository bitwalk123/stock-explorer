import statistics

from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_dataset_from_trade_with_id_code_start_end,
    get_sql_select_id_code_from_ticker,
    get_sql_select_max_date_from_trade_with_id_code_start_end,
    get_sql_select_open_from_trade_with_id_code_date,
    get_sql_select_volume_from_trade_with_id_code_start_end,
)
from functions.resources import get_connection


def get_basic_dataset(list_id_code: list, start: int, end: int):
    list_series = list()
    for id_code in list_id_code[0:1]:
        con = get_connection()
        if con.open():
            sql = get_sql_select_dataset_from_trade_with_id_code_start_end(id_code, start, end)
            query = QSqlQuery(sql)
            list_id_date = list()
            list_id_open = list()
            list_id_high = list()
            list_id_low = list()
            list_id_close = list()
            while query.next():
                list_id_date.append(query.value(0))
                list_id_open.append(query.value(1))
                list_id_high.append(query.value(2))
                list_id_low.append(query.value(3))
                list_id_close.append(query.value(4))

            con.close()

            print(list_id_date)


def get_valid_list_id_code(start: int, end: int, count_min: int, volume_min: int) -> list:
    """Get valid set of id_code with specified conditions

    Args:
        start (int): start time
        count_min (int): minimum count of data
        volume_min (int): minimum volume in median

    Returns:
        list: list of valid id_code

    """
    con = get_connection()
    if con.open():
        sql1 = get_sql_select_id_code_from_ticker()
        query1 = QSqlQuery(sql1)
        list_id_code = list()
        while query1.next():
            id_code = query1.value(0)

            sql2 = get_sql_select_volume_from_trade_with_id_code_start_end(id_code, start, end)
            query2 = QSqlQuery(sql2)
            list_volume = list()
            while query2.next():
                list_volume.append(query2.value(0))

            if len(list_volume) < count_min:
                continue
            volume_median = statistics.median(list_volume)
            if volume_median < volume_min:
                continue
            list_id_code.append(id_code)

        con.close()
        return list_id_code


def get_target_list_id_code(list_id_code: list, price_min: int, price_max: int, start: int, end: int) -> list:
    list_id_code_target = list()
    con = get_connection()
    if con.open():
        for id_code in list_id_code:
            sql1 = get_sql_select_max_date_from_trade_with_id_code_start_end(id_code, start, end)
            query1 = QSqlQuery(sql1)
            while query1.next():
                date = query1.value(0)
                sql2 = get_sql_select_open_from_trade_with_id_code_date(id_code, date)
                query2 = QSqlQuery(sql2)
                while query2.next():
                    price_open = query2.value(0)
                    if price_min < price_open < price_max:
                        list_id_code_target.append(id_code)

        con.close()
        return list_id_code_target
