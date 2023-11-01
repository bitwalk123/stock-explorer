import os
import pickle

import pandas as pd
from PySide6.QtSql import QSqlQuery
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler

from database.sqls import (
    get_sql_select_id_predict_from_predict_with_id_code_date,
    get_sql_update_predict_values,
    get_sql_insert_into_predict_values,
)
from functions.get_dataset import combine_ticker_data
from functions.get_dict_code import get_dict_code
from functions.get_valid_code import get_valid_code
from functions.prediction import search_minimal_component_number
from functions.resources import get_connection


def get_valid_dataset(start, end) -> tuple:
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # Get list of valid code and target
    pkl_list_valid_id_code = 'pool/list_valid_id_code_%d.pkl' % end
    pkl_list_target_id_code = 'pool/list_target_id_code_%d.pkl' % end
    if os.path.isfile(pkl_list_valid_id_code) and os.path.isfile(pkl_list_target_id_code):
        dict_code: dict = get_dict_code()
        with open(pkl_list_valid_id_code, 'rb') as f:
            list_valid_id_code = pickle.load(f)
        with open(pkl_list_target_id_code, 'rb') as f:
            list_target_id_code = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        dict_code, list_valid_id_code, list_target_id_code = get_valid_code(start, end)
        with open(pkl_list_valid_id_code, 'wb') as f:
            pickle.dump(list_valid_id_code, f)
        with open(pkl_list_target_id_code, 'wb') as f:
            pickle.dump(list_target_id_code, f)

    print('number of valid id_code : %d' % len(list_valid_id_code))
    print('number of target id_code : %d' % len(list_target_id_code))

    return dict_code, list_valid_id_code, list_target_id_code


def get_base_dataframe(list_valid_id_code, start, end) -> pd.DataFrame:
    # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
    # Get base dataframe
    pkl_df_base = 'pool/df_base_%d.pkl' % end
    if os.path.isfile(pkl_df_base):
        with open(pkl_df_base, 'rb') as f:
            df_base = pickle.load(f)
    else:
        if not os.path.isdir('pool'):
            os.mkdir('pool')
        df_base: pd.DataFrame = combine_ticker_data(list_valid_id_code, start, end)
        with open(pkl_df_base, 'wb') as f:
            pickle.dump(df_base, f)
    print(df_base)
    print(df_base.shape)
    return df_base


def get_prediction_by_pls(df_base, dict_code, end_next, list_target_id_code):
    columns_summary_code = ['Components', 'RMSE', 'R2', 'Open']
    df_summary_code = pd.DataFrame(columns=columns_summary_code)
    for target_id_code in list_target_id_code:
        name_open = '%d_open' % target_id_code
        df_base_2 = df_base.drop(name_open, axis=1)
        # Preparing Training & Test datasets
        df_X_train = df_base_2.iloc[0:len(df_base_2) - 1, :]
        df_X_test = df_base_2.tail(1)
        # Standardization
        scaler = StandardScaler()
        scaler.fit(df_X_train)
        X_train = scaler.transform(df_X_train)
        X_test = scaler.transform(df_X_test)
        # Pas data for Training
        y_train = df_base[name_open].iloc[1:]
        # PLS model with optimal n_comp to minimize MSE
        index_mse_min = search_minimal_component_number(X_train, y_train)
        n_comp = index_mse_min + 1
        pls = PLSRegression(n_components=n_comp)
        pls.fit(X_train, y_train)
        # Prediction and Correlation score (R square)
        y_pred = pls.predict(X_train)
        r2 = r2_score(y_train, y_pred)
        rmse = mean_squared_error(y_train, y_pred, squared=False)
        # Predict Open price for tomorrow
        price_open_pred = pls.predict(X_test)[0]
        series_fitting = pd.Series(
            data=[n_comp, rmse, r2, price_open_pred],
            index=columns_summary_code,
            name=dict_code[target_id_code]
        )

        con = get_connection()
        if con.open():
            sql1 = get_sql_select_id_predict_from_predict_with_id_code_date(
                target_id_code, end_next
            )
            query1 = QSqlQuery()
            query1.exec(sql1)
            if query1.next():
                id_predict = query1.value(0)
                sql2 = get_sql_update_predict_values(
                    id_predict, series_fitting
                )
            else:
                sql2 = get_sql_insert_into_predict_values(
                    target_id_code, end_next, series_fitting
                )
            # execute query
            query2 = QSqlQuery()
            query2.exec(sql2)
            con.close()

        df_summary_code.loc[dict_code[target_id_code]] = series_fitting
        print(df_summary_code)


def get_prediction_by_pls_2(df_base, dict_code, target_id_code):
    columns_summary_code = ['Components', 'RMSE', 'R2', 'Open']
    # df_summary_code = pd.DataFrame(columns=columns_summary_code)
    name_open = '%d_open' % target_id_code
    df_base_2 = df_base.drop(name_open, axis=1)
    # Preparing Training & Test datasets
    df_X_train = df_base_2.iloc[0:len(df_base_2) - 1, :]
    df_X_test = df_base_2.tail(1)
    # Standardization
    scaler = StandardScaler()
    scaler.fit(df_X_train)
    X_train = scaler.transform(df_X_train)
    X_test = scaler.transform(df_X_test)
    # Pas data for Training
    y_train = df_base[name_open].iloc[1:]
    # PLS model with optimal n_comp to minimize MSE
    index_mse_min = search_minimal_component_number(X_train, y_train)
    n_comp = index_mse_min + 1
    pls = PLSRegression(n_components=n_comp)
    pls.fit(X_train, y_train)
    # Prediction and Correlation score (R square)
    y_pred = pls.predict(X_train)
    r2 = r2_score(y_train, y_pred)
    rmse = mean_squared_error(y_train, y_pred, squared=False)
    # Predict Open price for tomorrow
    price_open_pred = pls.predict(X_test)[0]
    series_fitting = pd.Series(
        data=[n_comp, rmse, r2, price_open_pred],
        index=columns_summary_code,
        name=dict_code[target_id_code]
    )

    # df_summary_code.loc[dict_code[target_id_code]] = series_fitting
    # print(df_summary_code)
    return series_fitting
