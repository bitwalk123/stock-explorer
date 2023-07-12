from PySide6.QtSql import QSqlQuery

from functions.resources import get_connection


def get_open_with_code(code: int) -> tuple:
    """Get Date and Open data specified with code

    Args:
        code (int): ticker number

    Returns:
        cname (str): Company name
        list_x (list): List of Date in integer from Unix epoch date
        list_y (list): List of stock price
    """
    cname = None
    list_x = list()
    list_y = list()
    con = get_connection()
    if con.open():
        # get id_code == id_ticker
        id_ticker = 0
        sql = 'SELECT id_ticker, 銘柄名 FROM ticker WHERE コード=%d;' % code
        query = QSqlQuery(sql)
        while query.next():
            id_ticker = query.value(0)
            cname = query.value(1)
            # print(id_ticker)
            break
        # get list of Date & Open specified with id_code
        sql = 'SELECT date, open FROM trade WHERE id_code=%d ORDER BY date;' % id_ticker
        query = QSqlQuery(sql)
        while query.next():
            list_x.append(query.value(0))
            list_y.append(query.value(1))

        con.close()

    return cname, list_x, list_y
