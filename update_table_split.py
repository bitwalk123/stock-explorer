from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_insert_into_split_values, get_sql_select_lastsplit_split_with_id_code,
)
from functions.get_dict_code import get_dict_code
from functions.get_info_ticker import get_info_ticker
from functions.resources import get_connection


def main():
    # generate dict for code with id_code
    con = get_connection()
    if con.open():
        # prepare dictionary for id_code and code
        dict_code = get_dict_code()
        # fill infor to split table
        query = QSqlQuery()
        sql = get_sql_insert_into_split_values()
        query.prepare(sql)
        key_split_date = 'lastSplitDate'
        key_split_factor = 'lastSplitFactor'
        for id_code in dict_code.keys():
            sql2 = get_sql_select_lastsplit_split_with_id_code(id_code)
            query2 = QSqlQuery(sql2)
            id_split = None
            last_split_date = None
            last_split_factor = None
            while query2.next():
                id_split = query2.value(0)
                last_split_date = query2.value(1)
                last_split_factor = query2.value(2)
            if type(id_split) is int:
                code = dict_code[id_code]
                dict_info = get_info_ticker(code)
                if key_split_date not in dict_info.keys():
                    print('S', id_split, '%d.T' % code)
                    continue
                print(id_split, '%d.T' % code)
                if last_split_date != dict_info[key_split_date] or last_split_factor != dict_info[key_split_factor]:
                    query3 = QSqlQuery()
                    sql31 = 'UPDATE split SET lastSplitDate=%d WHERE id_split=%d;' % (
                        dict_info[key_split_date], id_split
                    )
                    query3.exec(sql31)
                    sql32 = 'UPDATE split SET lastSplitFactor="%s" WHERE id_split=%d;' % (
                        dict_info[key_split_factor], id_split
                    )
                    query3.exec(sql32)
                    print(
                        'U', id_split, id_code,
                        last_split_date, '>', dict_info[key_split_date],
                        last_split_factor, '>', dict_info[key_split_factor]
                    )
            else:
                code = dict_code[id_code]
                dict_info = get_info_ticker(code)
                if key_split_date in dict_info.keys():
                    query.bindValue(0, id_code)
                    query.bindValue(1, dict_info[key_split_date])
                    query.bindValue(2, dict_info[key_split_factor])
                    query.exec()
                    print(id_code, dict_info[key_split_date], dict_info[key_split_factor])

        con.close()


if __name__ == "__main__":
    main()
