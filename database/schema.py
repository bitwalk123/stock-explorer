from PySide6.QtSql import QSqlQuery

from functions.resources import get_connection


def initialize_db():
    con = get_connection(flag_delete=True)
    if not con.open():
        return

    sql = """
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
    query = QSqlQuery()
    query.exec(sql)
    con.close()
