import datetime as dt
from functions.predict_price import (
    get_base_dataframe,
    get_valid_dataset,
)
from functions.resources import get_connection
from functions.trading_date import (
    get_last_trading_date,
    get_next_trading_date,
)

day1 = 24 * 60 * 60
con = get_connection()
if con.open():
    end: int = get_last_trading_date()
    start = end - 365 * 2 * day1
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
else:
    print('fail to open db.')

