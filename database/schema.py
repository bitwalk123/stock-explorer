import os

import pandas as pd
import wget
from PySide6.QtSql import QSqlDatabase, QSqlQuery

from functions.handle_file import delete_file
from functions.resources import get_info

con = QSqlDatabase.addDatabase('QSQLITE')


def initialize_db():
    dbname = get_info('db')
    delete_file(dbname)

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


def update_tse():
    url = get_info('tse')
    basename = os.path.basename(url)
    delete_file(basename)
    filename = wget.download(url)
    print(filename)
    df_all = pd.read_excel(filename)
    delete_file(filename)

    """
    list_market = [
        'グロース（内国株式）',
        'グロース（外国株式）',
        'スタンダード（内国株式）',
        'スタンダード（外国株式）',
        'プライム（内国株式）',
        'プライム（外国株式）',
    ]
    """
    list_market = [
        'プライム（内国株式）',
        'プライム（外国株式）',
    ]
    df_stock = df_all[df_all['市場・商品区分'].isin(list_market)].reset_index(drop=True)

    dbname = get_info('db')
    con.setDatabaseName(dbname)
    if not con.open():
        return

    query = QSqlQuery()

    for r in df_stock.index:
        series = df_stock.loc[r]
        sql = 'INSERT INTO ticker values(NULL, %d, %d, "%s", "%s", %d, "%s", %d, "%s", "%s", "%s")' % (
            series['日付'],
            series['コード'],
            series['銘柄名'],
            series['市場・商品区分'],
            series['33業種コード'],
            series['33業種区分'],
            series['17業種コード'],
            series['17業種区分'],
            series['規模コード'],
            series['規模区分']
        )
        query.exec(sql)

    con.close()
