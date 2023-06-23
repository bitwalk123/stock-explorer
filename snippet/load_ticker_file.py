import os

import pandas as pd
from PySide6.QtSql import QSqlQuery

from functions.prediction import search_optimal_components, optimal_scores
from functions.resources import get_connection

con = get_connection()
if con.open():
    list_ticker = list()
    sql = 'select コード from ticker;'
    query = QSqlQuery(sql)
    while query.next():
        list_ticker.append(query.value(0))
    con.close()

    list_close = list()
    ticker_target = list_ticker[2000]
    df_open_0 = None
    for ticker in list_ticker:
        filename = '%s.csv' % os.path.join('data', '%d.T' % ticker)
        df = pd.read_csv(filename, index_col=0)
        if ticker == ticker_target:
            df_open_0 = df['Open'].rename(ticker)
        else:
            list_close.append(df['Close'].rename(ticker))

    df_close = pd.concat(list_close, axis=1)
    list_head = df_close.columns

    df_all = df_close.iloc[1:len(df_close), ]
    df_open = df_open_0[0:len(df_open_0) - 1]
    df_all[ticker_target] = df_open.values
    df_all.dropna(how='any', axis=1, inplace=True)
    print(df_all)

    X = df_all.iloc[:, 0:len(df_close) - 1].values
    y = df_all[ticker_target].values

    mse_min_x, mse_min_y = search_optimal_components(X, y)
    print(mse_min_x[0], mse_min_y[0])

    n_comp = mse_min_x[0] + 1
    x_drop = mse_min_y[0]
    sorted_ind = optimal_scores(X, y, n_comp, x_drop)
    print(sorted_ind, len(sorted_ind))
    print(sorted_ind[x_drop:], len(sorted_ind[x_drop:]))
    print(list_head[sorted_ind[x_drop:]])
