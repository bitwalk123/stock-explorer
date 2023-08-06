from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_select_id_code_from_ticker, get_sql_select_id_trade_date_open_from_trade_with_id_code, get_sql_delete_trade_with_id_trade
from functions.resources import get_connection


def check_duplicate_trade():
    con = get_connection()
    if con.open():
        sql1 = get_sql_select_id_code_from_ticker()
        query1 = QSqlQuery(sql1)
        while query1.next():
            id_code = query1.value(0)
            print(id_code)

            list_date = list()
            sql2 = get_sql_select_id_trade_date_open_from_trade_with_id_code(id_code)
            query2 = QSqlQuery(sql2)
            while query2.next():
                id_trade = query2.value(0)
                date = query2.value(1)
                open = query2.value(2)
                if date in list_date:
                    print('duplicate', id_trade, date, open)
                    sql3 = get_sql_delete_trade_with_id_trade(id_trade)
                    query3 = QSqlQuery()
                    query3.exec(sql3)
                else:
                    list_date.append(date)

        con.close()
