from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_select_id_code_code_from_ticker,
    get_sql_insert_into_split_values,
)
from functions.get_info_ticker import get_info_ticker
from functions.resources import get_connection


def main():
    # generate dict for code with id_code
    dict_code = dict()
    list_id_code = list()
    con = get_connection()
    if con.open():
        # prepare dictionary for id_code and code
        sql1 = get_sql_select_id_code_code_from_ticker()
        query1 = QSqlQuery(sql1)
        while query1.next():
            id_code = query1.value(0)
            list_id_code.append(id_code)
            code = query1.value(1)
            dict_code[id_code] = code

        # fill infor to split table
        query2 = QSqlQuery()
        sql2 = get_sql_insert_into_split_values()
        query2.prepare(sql2)
        key_split_date = 'lastSplitDate'
        key_split_factor = 'lastSplitFactor'
        for id_code in list_id_code:
            code = dict_code[id_code]
            dict_info = get_info_ticker(code)
            if key_split_date in dict_info.keys():
                query2.bindValue(0, id_code)
                query2.bindValue(1, dict_info[key_split_date])
                query2.bindValue(2, dict_info[key_split_factor])
                query2.exec()
                print(id_code, dict_info[key_split_date], dict_info[key_split_factor])

        con.close()


if __name__ == "__main__":
    main()