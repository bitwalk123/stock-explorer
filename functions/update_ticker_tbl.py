import sys

from PySide6.QtSql import QSqlQuery

from database.sqls_ticker import (
    delete_ticker_with_code,
    insert_into_ticker_values,
    select_code_from_ticker,
    select_id_code_from_ticker_with_code,
    update_ticker_values,
)
from functions.resources import (
    get_connection,
    get_tse_data,
)


def update_ticker_tbl():
    df_all = get_tse_data()
    list_market = [
        'グロース（内国株式）',
        'グロース（外国株式）',
        'スタンダード（内国株式）',
        'スタンダード（外国株式）',
        'プライム（内国株式）',
        'プライム（外国株式）',
    ]
    df_stock = df_all[
        df_all['市場・商品区分'].isin(list_market) &
        (df_all['コード'] < 10000)
        ].reset_index(drop=True)
    list_row = list(df_stock.index)

    con = get_connection()
    if con.open():
        query = QSqlQuery()
        for count, row in enumerate(list_row):
            series = df_stock.loc[row]
            code = series['コード']
            sql = select_id_code_from_ticker_with_code(code)
            query.exec(sql)
            if query.next():
                id_code = query.value(0)
                sql = update_ticker_values(id_code, series)
            else:
                print(code, 'does not exist!')
                sql = insert_into_ticker_values(series)

            query.exec(sql)

        # get current list of ticker code
        list_code_current = list()
        sql = select_code_from_ticker()
        query.exec(sql)
        while query.next():
            code = query.value(0)
            list_code_current.append(code)

        # check code already de-listed
        list_code_new = list(df_stock['コード'])
        for code in list_code_current:
            if not (code in list_code_new):
                print(code, 'should be deleted!')
                sql = delete_ticker_with_code(code)
                query.exec(sql)

        con.close()
    else:
        print('database can not be opened!')
        sys.exit()
