import pickle
import time

import pandas as pd

from funcs.tbl_ticker import get_dict_id_code
from funcs.tbl_trade import get_date_close_with_id_code_start


def correlation_1to1(code_target: str, start: int):
    # print(code_target, datetime.datetime.fromtimestamp(start))
    dict_id_code = get_dict_id_code()
    list_code = list(dict_id_code.keys())

    id_code_target = dict_id_code[code_target]
    df1 = get_date_close_with_id_code_start(id_code_target, start)
    df1.columns = [code_target]

    dict_result = dict()
    for code in list_code:
        id_code = dict_id_code[code]
        df2 = get_date_close_with_id_code_start(id_code, start)
        df2.columns = [code]

        df0 = pd.concat([df1, df2], axis=1, join='inner')
        corr = df0.corr().iloc[0, 1]
        dict_result[code] = [corr]

    df_result = pd.DataFrame(dict_result).T
    col_name = 'Correlation'
    df_result.columns = [col_name]
    df_result.sort_values(col_name, inplace=True)
    df_top = df_result.head(1)
    print(df_top)

    now = int(time.time())
    day1 = 24 * 60 * 60
    today = now - now % day1
    pkl_corr = 'pool/corr_%s-%d.pkl' % (code_target, today)

    with open(pkl_corr, mode='wb') as f:
        pickle.dump(df_result, f)
