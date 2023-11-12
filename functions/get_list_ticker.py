from PySide6.QtSql import QSqlQuery

from database.sqls_predict import select_id_code_from_predict
from database.sqls_ticker import select_code_cname_from_ticker
from functions.get_dict_code import get_dict_it_code_code
from functions.resources import get_connection


def get_list_ticker() -> dict:
    """Get ticker list

    Returns:
        dict_ticker (dict): ticker code is a key and company name is a value.
    """
    dict_ticker = dict()
    con = get_connection()
    if con.open():
        sql = select_code_cname_from_ticker()
        query = QSqlQuery(sql)
        while query.next():
            code = query.value(0)
            cname = query.value(1)
            dict_ticker[code] = cname
        con.close()
        return dict_ticker
    else:
        print('database cannot be opened!')
        return dict()


def get_list_ticker_predicted() -> list:
    set_id_code_predicted = set()
    list_ticker_predicted = list()
    con = get_connection()
    if con.open():
        sql = select_id_code_from_predict()
        query = QSqlQuery(sql)
        while query.next():
            id_code = query.value(0)
            set_id_code_predicted.add(id_code)
        dict_code = get_dict_it_code_code()
        con.close()

        for id_code in sorted(list(set_id_code_predicted)):
            list_ticker_predicted.append(dict_code[id_code])

        return list_ticker_predicted
    else:
        print('database cannot be opened!')
        return list()
