import pandas as pd
import statistics

from PySide6.QtSql import QSqlQuery
from sklearn.preprocessing import StandardScaler

from database.sqls import (
    select_dataset_from_trade_with_id_code_start_end,
    select_date_from_split_with_id_code,
    select_id_code_from_ticker,
    select_max_date_from_trade_with_id_code_start_end,
    select_open_from_trade_with_id_code_date,
    select_volume_from_trade_with_id_code_start_end,
)
from functions.prediction import (
    minimal_scores,
    search_minimal_component_number,
)
from functions.resources import get_connection


def combine_ticker_data(list_id_code: list, start: int, end: int) -> pd.DataFrame:
    list_series = list()
    for id_code in list_id_code:
        con = get_connection()
        if con.open():
            sql = select_dataset_from_trade_with_id_code_start_end(id_code, start, end)
            query = QSqlQuery(sql)
            list_id_date = list()
            list_id_open = list()
            list_id_high = list()
            list_id_low = list()
            list_id_close = list()
            while query.next():
                list_id_date.append(query.value(0))
                list_id_open.append(query.value(1))
                list_id_high.append(query.value(2))
                list_id_low.append(query.value(3))
                list_id_close.append(query.value(4))
            con.close()

            series_open = pd.Series(
                data=list_id_open,
                index=list_id_date,
                name='%d_open' % id_code
            )
            series_high = pd.Series(
                data=list_id_high,
                index=list_id_date,
                name='%d_high' % id_code
            )
            series_low = pd.Series(
                data=list_id_low,
                index=list_id_date,
                name='%d_low' % id_code
            )
            series_close = pd.Series(
                data=list_id_close,
                index=list_id_date,
                name='%d_close' % id_code
            )

            #print(id_code, len(series_open), len(series_high), len(series_low), len(series_close))
            list_series.append(series_open)
            list_series.append(series_high)
            list_series.append(series_low)
            list_series.append(series_close)

    if len(list_series) == 0:
        print('list_series', 0)
        return pd.DataFrame()
    else:
        df = pd.concat(list_series, axis=1)
        df.dropna(how='any', axis=0, inplace=True)
        return df


def get_valid_list_id_code(start: int, end: int, count_min: int, volume_min: int) -> list:
    """Get valid set of id_code with specified conditions

    Args:
        start (int): start time
        count_min (int): minimum count of data
        volume_min (int): minimum volume in median

    Returns:
        list: list of valid id_code

    """
    con = get_connection()
    if con.open():
        sql1 = select_id_code_from_ticker()
        query1 = QSqlQuery(sql1)
        list_id_code = list()
        while query1.next():
            id_code = query1.value(0)
            # split check
            sql2 = select_date_from_split_with_id_code(id_code)
            query2 = QSqlQuery(sql2)
            split_flag = False
            while query2.next():
                date_split = query2.value(0)
                if type(date_split) is int:
                    if start <= date_split <= end:
                        split_flag = True

            if split_flag is True:
                print('split flag!', id_code)
                continue

            # volume check
            sql3 = select_volume_from_trade_with_id_code_start_end(id_code, start, end)
            query3 = QSqlQuery(sql3)
            list_volume = list()
            while query3.next():
                list_volume.append(query3.value(0))

            if len(list_volume) < count_min:
                continue
            volume_median = statistics.median(list_volume)
            if volume_median < volume_min:
                continue
            list_id_code.append(id_code)

        con.close()
        return list_id_code


def get_valid_list_id_code_wo_split(start: int, end: int, count_min: int, volume_min: int) -> list:
    """Get valid set of id_code with specified conditions

    Args:
        start (int): start time
        count_min (int): minimum count of data
        volume_min (int): minimum volume in median

    Returns:
        list: list of valid id_code

    """
    con = get_connection()
    if con.open():
        sql1 = select_id_code_from_ticker()
        query1 = QSqlQuery(sql1)
        list_id_code = list()
        while query1.next():
            id_code = query1.value(0)
            # volume check
            sql3 = select_volume_from_trade_with_id_code_start_end(id_code, start, end)
            query3 = QSqlQuery(sql3)
            list_volume = list()
            while query3.next():
                list_volume.append(query3.value(0))

            if len(list_volume) < count_min:
                continue
            volume_median = statistics.median(list_volume)
            if volume_median < volume_min:
                continue
            list_id_code.append(id_code)

        con.close()
        return list_id_code


def get_target_list_id_code(list_id_code: list, price_min: int, price_max: int, start: int, end: int) -> list:
    list_id_code_target = list()
    con = get_connection()
    if con.open():
        for id_code in list_id_code:
            sql1 = select_max_date_from_trade_with_id_code_start_end(id_code, start, end)
            query1 = QSqlQuery(sql1)
            while query1.next():
                date = query1.value(0)
                sql2 = select_open_from_trade_with_id_code_date(id_code, date)
                query2 = QSqlQuery(sql2)
                while query2.next():
                    price_open = query2.value(0)
                    if price_min < price_open < price_max:
                        list_id_code_target.append(id_code)

        con.close()
        return list_id_code_target


def get_candidate_tickers(list_id_code_target: list, df_base: pd.DataFrame) -> pd.DataFrame:
    columns_result = ['Components', 'R2 calib', 'R2 CV', 'MSE calib', 'MSE CV']
    df_result = pd.DataFrame(columns=columns_result)

    for id_code_target in list_id_code_target:
        name = '%d_open' % id_code_target
        series_y = df_base[name].iloc[1:]
        df_X = df_base.iloc[0:len(df_base) - 1, :]

        scaler = StandardScaler()
        scaler.fit(df_X)
        X = scaler.transform(df_X)
        y = series_y

        index_mse_min = search_minimal_component_number(X, y)
        n_comp = index_mse_min + 1
        result = minimal_scores(X, y, n_comp)
        series_target = pd.Series(
            data=[n_comp, result['R2 calib'], result['R2 CV'], result['MSE calib'], result['MSE CV']],
            index=columns_result,
            name=id_code_target
        )
        df_result.loc[id_code_target] = series_target

    # save result
    df_result.to_csv('pool/result_pls.csv')
    return df_result
