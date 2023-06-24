import os

import pandas as pd
from PySide6.QtSql import QSqlQuery

from functions.prediction import search_optimal_components, optimal_scores, search_minimal_component_number, \
    minimal_scores
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
    ticker_target = list_ticker[500]
    df_open_0 = None
    label_ticker_target = None
    for ticker in list_ticker:
        filename = '%s.csv' % os.path.join('data', '%d.T' % ticker)
        df = pd.read_csv(filename, index_col=0)
        if ticker == ticker_target:
            label_ticker_target = '%d Open' % ticker
            df_open_0 = df['Open'].rename(label_ticker_target)

        list_close.append(df['Close'].rename(ticker))

    df_close = pd.concat(list_close, axis=1)
    list_head = df_close.columns

    df_all = df_close.iloc[0:len(df_close) - 1, ]
    df_open = df_open_0[1:len(df_open_0)]
    df_all[label_ticker_target] = df_open.values
    df_all.dropna(how='any', axis=1, inplace=True)
    print(df_all)

    X = df_all.iloc[:, 0:len(df_all.columns) - 1].values
    y = df_all[label_ticker_target].values
    print(X.shape)
    print(y.shape)

    mse_min = search_minimal_component_number(X, y)
    # mse_min_x, mse_min_y = search_optimal_components(X, y)
    # print(mse_min_x[0], mse_min_y[0])

    n_comp = mse_min + 1
    print('Suggested number of components: ', n_comp)

    # x_drop = mse_min_y[0]
    # result = optimal_scores(X, y, n_comp, x_drop)
    minimal_scores(X, y, n_comp)
    # print(sorted_ind, len(sorted_ind))
    # print(sorted_ind[x_drop:], len(sorted_ind[x_drop:]))
    # print(list_head[sorted_ind[x_drop:]])
    # print(ticker_target)
    # print('R2 calib: %5.3f' % result['R2 calib'])
    # print('R2 CV: %5.3f' % result['R2 CV'])
    # print('MSE calib: %5.3f' % result['MSE calib'])
    # rint('MSE CV: %5.3f' % result['MSE CV'])
