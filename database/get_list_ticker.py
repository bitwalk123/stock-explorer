from PySide6.QtSql import QSqlQuery

from functions.resources import get_connection


def get_list_ticker() -> dict:
    """Get ticker list

    Returns:
        dict_ticker (dict): ticker code is a key and company name is a value.
    """
    dict_ticker = dict()
    con = get_connection()
    if con.open():
        sql = 'select コード, 銘柄名 from ticker;'
        query = QSqlQuery(sql)
        while query.next():
            code = query.value(0)
            cname = query.value(1)
            dict_ticker[code] = cname
        con.close()
        return dict_ticker
    else:
        return dict()
