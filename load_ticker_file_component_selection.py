import os
import sys

import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls import select_code_from_ticker
from functions.prediction import (
    search_minimal_component_number,
    minimal_scores,
)
from functions.resources import get_connection

con = get_connection()
if not con.open():
    sys.exit()

list_code = list()

sql = select_code_from_ticker()
query = QSqlQuery(sql)
while query.next():
    code = query.value(0)
    filename = '%s.csv' % os.path.join('data', '%d.T' % code)
    df = pd.read_csv(filename, index_col=0)
    if len(df) > 360:
        list_code.append(code)
con.close()

list_close = list()
for code in list_code:
    filename = '%s.csv' % os.path.join('data', '%d.T' % code)
    df = pd.read_csv(filename, index_col=0)
    list_close.append(df['Close'].rename(code))

df_close = pd.concat(list_close, axis=1)
print(df_close)

# empty dataframe
columns_result = ['Components', 'R2 calib', 'R2 CV', 'MSE calib', 'MSE CV']
df_result = pd.DataFrame(columns=columns_result)

# loop for each ticker
for code_target in list_code:
    filename = '%s.csv' % os.path.join('data', '%d.T' % code_target)
    series_open_target = pd.read_csv(filename, index_col=0)['Open']
    label_code_target = '%d Open' % code_target

    df_all = df_close.iloc[0:len(df_close) - 1, :].copy()
    df_open = series_open_target[1:len(series_open_target)]
    df_all[label_code_target] = df_open.values
    df_all.dropna(how='any', axis=1, inplace=True)

    X = df_all.iloc[:, 0:len(df_all.columns) - 1].values
    y = df_all[label_code_target].values
    print(X.shape)
    print(y.shape)

    mse_min = search_minimal_component_number(X, y)

    n_comp = mse_min + 1
    result = minimal_scores(X, y, n_comp)
    series_target = pd.Series(
        data=[n_comp, result['R2 calib'], result['R2 CV'], result['MSE calib'], result['MSE CV']],
        index=columns_result,
        name=code_target
    )
    df_result.loc[code_target] = series_target
    print(df_result)
    # save result every time
    df_result.to_csv('result_pls.csv')
