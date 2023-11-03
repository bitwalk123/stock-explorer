import datetime as dt
import pandas as pd
import time

from PySide6.QtSql import QSqlQuery

from database.sqls_trade import select_dataset_from_trade_with_id_code_start_end
from functions.get_elapsed import get_elapsed
from functions.predict_price import get_valid_dataset
from functions.resources import get_connection
from functions.trading_date import (
    get_last_trading_date,
    get_next_trading_date,
)


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

            # print(id_code, len(series_open), len(series_high), len(series_low), len(series_close))
            list_series.append(series_open)
            list_series.append(series_high)
            list_series.append(series_low)
            list_series.append(series_close)

    if len(list_series) == 0:
        print('list_series', 0)
        return pd.DataFrame()
    else:
        df = pd.concat(list_series, axis=1)
        df.dropna(how='any', axis=1, inplace=True)
        return df


def get_base_dataframe(list_valid_id_code, start, end) -> pd.DataFrame:
    df_base: pd.DataFrame = combine_ticker_data(list_valid_id_code, start, end)
    print(df_base)
    print(df_base.shape)
    return df_base


def update_prediction():
    day1 = 24 * 60 * 60
    con = get_connection()
    if con.open():
        end: int = get_last_trading_date()
        start = end - 365 * day1
        print(
            'date scope :',
            dt.datetime.fromtimestamp(start),
            '-',
            dt.datetime.fromtimestamp(end)
        )
        end_next = get_next_trading_date(end)

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Get list of valid code and target
        dict_code, list_valid_id_code, list_target_id_code = get_valid_dataset(start, end)
        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Generate base dataframe
        df_base = get_base_dataframe(list_valid_id_code, start, end)
        con.close()

        print('last date', [dt.datetime.fromtimestamp(d) for d in df_base.index].pop())

        # _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
        # Prediction for next Open price
        # get_prediction_by_pls(df_base, dict_code, end_next, list_target_id_code)
    else:
        print('fail to open db.')


if __name__ == '__main__':
    time_start = time.time()
    end = dt.date.today()
    update_prediction()
    print('elapsed %.3f sec' % get_elapsed(time_start))
