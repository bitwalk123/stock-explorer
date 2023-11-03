import datetime as dt
import os
import sys

import pandas as pd
import pickle
import time

from PySide6.QtSql import QSqlQuery
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

from database.sqls_trade import (
    select_min_date_from_trade_with_id_code_end,
    select_open_from_trade_with_id_code_date,
)
from functions.conv_timestamp2date import conv_timestamp2date
from functions.get_dataset import (
    get_valid_list_id_code,
    combine_ticker_data,
)
from functions.get_dict_code import get_dict_code
from functions.get_elapsed import get_elapsed
from functions.resources import get_connection


def main():
    """Simulate prediction performance using past data
    """
    # Constants
    count_min = 200
    volume_min = 10000

    tz_delta = 9 * 60 * 60  # Asia/Tokyo timezone
    day = 24 * 60 * 60
    year = 365 * day

    end_str = '2023-01-04'
    end_dt = dt.datetime.strptime(end_str, '%Y-%m-%d')

    # Loop condition
    duration = 250 * day
    origin = end = int(dt.datetime.timestamp(end_dt)) + tz_delta

    while end < origin + duration:
        start = end - year
        print()
        print(conv_timestamp2date(start), conv_timestamp2date(end))
        end_next = 0

        # List valid id_code
        time_start = time.time()
        pkl_list_id_code = 'pool/list_id_code_%d.pkl' % end
        if os.path.isfile(pkl_list_id_code):
            with open(pkl_list_id_code, 'rb') as f:
                list_id_code = pickle.load(f)
        else:
            if not os.path.isdir('pool'):
                os.mkdir('pool')
            list_id_code = get_valid_list_id_code(start, end, count_min, volume_min)
            with open(pkl_list_id_code, 'wb') as f:
                pickle.dump(list_id_code, f)

        print('\nvalid total :', len(list_id_code))
        print('elapsed {:.3f}'.format(get_elapsed(time_start)), 'sec')

        # Base dataset
        time_start = time.time()
        pkl_df_base = 'pool/list_df_base_%d.pkl' % end
        if os.path.isfile(pkl_df_base):
            with open(pkl_df_base, 'rb') as f:
                df_base = pickle.load(f)
        else:
            df_base = combine_ticker_data(list_id_code, start, end)
            with open(pkl_df_base, 'wb') as f:
                pickle.dump(df_base, f)

        print(df_base)
        print('elapsed {:.3f}'.format(get_elapsed(time_start)), 'sec')

        # ticker selection and performance
        pkl_df_sel = 'pool/df_sel-%d.csv' % origin
        if os.path.isfile(pkl_df_sel):
            with open(pkl_df_sel, 'rb') as f:
                df_sel = pickle.load(f)
        else:
            sys.exit()

        print(df_sel)

        dict_code = dict()
        con = get_connection()
        if con.open():
            dict_code = get_dict_code()
        con.close()

        for id_code in df_sel.index:
            code = dict_code[id_code]
            n_comp = int(df_sel.loc[id_code, 'Components'])
            # _________________________________________________________________
            # Open price
            price_open = None
            con = get_connection()
            if con.open():
                # Get next trade day
                sql1 = select_min_date_from_trade_with_id_code_end(id_code, end)
                query1 = QSqlQuery(sql1)
                while query1.next():
                    end_next = query1.value(0)
                # Get open price in next trade day
                sql2 = select_open_from_trade_with_id_code_date(id_code, end_next)
                query2 = QSqlQuery(sql2)
                while query2.next():
                    price_open = query2.value(0)
            con.close()
            # _________________________________________________________________
            # Prediction for end
            name_open = '%d_open' % id_code
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
            # PLS model
            pls = PLSRegression(n_components=n_comp)
            pls.fit(X_train, y_train)
            # Prediction and Correlation score (R square)
            y_pred = pls.predict(X_train)
            r2 = r2_score(y_train, y_pred)
            # Predict Open price for tomorrow
            price_open_pred = pls.predict(X_test)[0][0]
            # _________________________________________________________________
            # Summary for code
            pkl_df_summary_code = 'pool/df_summary-%d.pkl' % code
            columns_summary_code = ['Components', 'R2', 'Open(pred)', 'Open', 'delta']
            if os.path.isfile(pkl_df_summary_code):
                with open(pkl_df_summary_code, 'rb') as f:
                    df_summary_code = pickle.load(f)
            else:
                df_summary_code = pd.DataFrame(columns=columns_summary_code)
            # Prepare 1 row in series
            series_code = pd.Series(
                data=[n_comp,
                      '{:.3f}'.format(r2),
                      '{:.1f}'.format(price_open_pred),
                      price_open,
                      '{:.1f}'.format(price_open_pred - price_open)],
                index=columns_summary_code,
                name=conv_timestamp2date(end_next)
            )
            # Write results
            df_summary_code.loc[conv_timestamp2date(end_next)] = series_code
            with open(pkl_df_summary_code, 'wb') as f:
                pickle.dump(df_summary_code, f)
            print('\n%d.T' % code)
            print(df_summary_code)
        # update end day
        if end < end_next:
            end = end_next
        else:
            end += day


if __name__ == "__main__":
    main()
