from PySide6.QtSql import QSqlQuery

from database.sqls import get_sql_select_id_code_code_from_ticker


def get_dict_code() -> dict:
    dict_code = dict()
    list_id_code = list()

    sql = get_sql_select_id_code_code_from_ticker()
    query = QSqlQuery(sql)
    while query.next():
        id_code = query.value(0)
        list_id_code.append(id_code)
        code = query.value(1)
        dict_code[id_code] = code
    return dict_code
