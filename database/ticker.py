import os

import pandas as pd
import wget
from PySide6.QtSql import QSqlDatabase, QSqlQuery

from functions.handle_file import delete_file
from functions.resources import get_info


def update_tse():
    url = get_info('tse')
    basename = os.path.basename(url)
    delete_file(basename)
    filename = wget.download(url)
    print(filename)
    df_all = pd.read_excel(filename)
    delete_file(filename)

    list_market = [
        'グロース（内国株式）',
        'グロース（外国株式）',
        'スタンダード（内国株式）',
        'スタンダード（外国株式）',
        'プライム（内国株式）',
        'プライム（外国株式）',
    ]
    df_stock = df_all[df_all['市場・商品区分'].isin(list_market)].reset_index(drop=True)

    dbname = get_info('db')
    con = QSqlDatabase.addDatabase('QSQLITE')
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
