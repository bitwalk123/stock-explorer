from PySide6.QtSql import QSqlQuery

from database.sqls import (
    get_sql_insert_into_split_values,
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
