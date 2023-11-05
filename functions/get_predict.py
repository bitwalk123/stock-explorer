import pandas as pd
from PySide6.QtSql import QSqlQuery

from database.sqls_predict import (
    select_all_from_predict_with_date,
    select_max_date_from_predict,
)
from database.sqls_ticker import select_id_code_code_cname_from_ticker
from functions.resources import get_connection


def get_predict_dataframe(date_predict: int) -> pd.DataFrame:
    con = get_connection()
    if con.open():
        dict_code = dict()
        dict_cname = dict()
        sql = select_id_code_code_cname_from_ticker()
        query = QSqlQuery(sql)
        while query.next():
            id_code = query.value(0)
            dict_code[id_code] = query.value(1)
            dict_cname[id_code] = query.value(2)

        list_code = list()
        list_cname = list()
        list_comp = list()
        list_rmse = list()
        list_r2 = list()
        list_open = list()
        sql = select_all_from_predict_with_date(date_predict)
        query.exec(sql)
        while query.next():
            id_code = query.value(0)
            comp = query.value(1)
            rmse = query.value(2)
            r2 = query.value(3)
            open = query.value(4)
            if id_code in dict_code.keys():
                # print(dict_code[id_code], dict_cname[id_code], comp, rmse, r2, open)
                list_code.append(dict_code[id_code])
                list_cname.append(dict_cname[id_code])
                list_comp.append(comp)
                list_rmse.append(rmse)
                list_r2.append(r2)
                list_open.append(open)
        con.close()

        df_pred = pd.DataFrame({
            'コード': list_code,
            '銘柄': list_cname,
            '成分数': list_comp,
            'RMSE': list_rmse,
            'R2': list_r2,
            '始値': list_open,
        })
        return df_pred
    else:
        return pd.DataFrame()


def get_predict_date_latest() -> int:
    date_predict = 0
    con = get_connection()
    if con.open():
        sql = select_max_date_from_predict()
        query = QSqlQuery(sql)
        if query.next():
            date_predict = query.value(0)
        con.close()
    return date_predict
