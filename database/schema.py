from PySide6.QtSql import QSqlDatabase, QSqlQuery

from functions.handle_file import delete_file
from functions.resources import get_info


def initialize_db():
    dbname = get_info('db')
    delete_file(dbname)

    con = QSqlDatabase.addDatabase('QSQLITE')
    con.setDatabaseName(dbname)
    if not con.open():
        return

    query = QSqlQuery()
    query.exec(
        """
        CREATE TABLE ticker(
            id_ticker INTEGER PRIMARY KEY AUTOINCREMENT,
            '日付' INTEGER,
            'コード' INTEGER,
            '銘柄名' STRING,
            '市場・商品区分' STRING,
            '33業種コード' INTEGER,
            '33業種区分' STRING,
            '17業種コード' INTEGER,
            '17業種区分' STRING,
            '規模コード' STRING,
            '規模区分' STRING
        )
        """
    )

    con.close()