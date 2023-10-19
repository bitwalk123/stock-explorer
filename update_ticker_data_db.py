import datetime as dt

from PySide6.QtSql import QSqlQuery

from functions.update_db import update_ticker

if __name__ == '__main__':
    end = dt.date.today()
    queries = [QSqlQuery() for k in range(4)]
    update_ticker(end, queries)
