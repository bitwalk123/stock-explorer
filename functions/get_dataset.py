import statistics

from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_select_id_code_from_ticker, get_sql_select_volume_from_trade_with_id_code_start, get_sql_select_max_date_from_trade_with_id_code, get_sql_select_open_from_trade_with_id_code_date
from functions.resources import get_connection


def get_valid_list_id_code(start: int, count_min: int, volume_min: int) -> list:
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

            sql2 = get_sql_select_volume_from_trade_with_id_code_start(id_code, start)
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


def get_target_list_id_code(list_id_code:list, price_min:int, price_max:int) -> list:
    list_id_code_target = list()
    con = get_connection()
    if con.open():
        for id_code in list_id_code:
            sql1 = get_sql_select_max_date_from_trade_with_id_code(id_code)
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
