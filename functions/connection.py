from PySide6.QtSql import QSqlDatabase

from functions.handle_file import delete_file
from functions.resources import get_info

con = QSqlDatabase.addDatabase('QSQLITE')


def get_connection(flag_delete=False) -> QSqlDatabase:
    dbname = get_info('db')
    if flag_delete:
        delete_file(dbname)

    con.setDatabaseName(dbname)
    return con
