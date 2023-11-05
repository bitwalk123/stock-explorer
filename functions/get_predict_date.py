from PySide6.QtSql import QSqlQuery

from database.sqls_predict import select_max_date_from_predict
from functions.resources import get_connection


def get_predict_date_latest() -> int:
    date_predict = 0
    con = get_connection()
    if con.open():
        sql = select_max_date_from_predict()
        query = QSqlQuery(sql)
        if query.next():
            date_predict = query.value(0)
        con.close()
    return date_predict
