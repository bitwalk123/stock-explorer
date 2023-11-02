import datetime as dt

import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls import (
    insert_into_contract_values,
    select_id_contract_from_contract_with_order_date,
    update_contract_values,
)
from functions.resources import get_connection


def read_csv_contract_from_shiftjis(filename: str) -> pd.DataFrame:
    columns = [
        '注文番号',
        '状況',
        '注文日時',
        '銘柄',
        '銘柄コード・市場',
        '売買',
        '口座',
        '注文方法',
        '注文数量[株/口]',
        '約定数量[株/口]',
        '注文単価[円]',
        '約定単価[円]',
        '約定代金[円]',
        '手数料[円]'
    ]
    df = pd.read_csv(filename, encoding='shift_jis')
    df2 = df[columns][df['状況'] == '約定']

    y = '2023'
    fmt = '%Y/%m/%d %H:%M'
    col = '注文日時'
    df2[col] = [int(dt.datetime.timestamp(dt.datetime.strptime('%s/%s' % (y, t), fmt))) for t in df2[col]]
    con = get_connection()
    if con.open():
        for row_index in df2.index:
            series = df2.loc[row_index]

            num_order = int(series['注文番号'])
            date_order = int(series['注文日時'])
            sql1 = select_id_contract_from_contract_with_order_date(num_order, date_order)
            query1 = QSqlQuery()
            query1.exec(sql1)
            if query1.next():
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # if data exists, update the trade table
                id_contract = query1.value(0)
                print('UPDATE id_contract =', id_contract)
                sql2 = update_contract_values(id_contract, series)
            else:
                # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
                # if not, append data to the trade table
                sql2 = insert_into_contract_values(series)
            # execute query
            query2 = QSqlQuery()
            query2.exec(sql2)

        con.close()

    # df2.to_csv('out.csv', index=False)
    return df2
