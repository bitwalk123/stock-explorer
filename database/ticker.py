import os

import pandas as pd
import wget

from functions.handle_file import delete_file
from functions.resources import get_info


def update_tse():
    url = get_info('tse')
    basename = os.path.basename(url)
    delete_file(basename)
    filename = wget.download(url)
    print(filename)
    df = pd.read_excel(filename)
    delete_file(filename)
    print(df.columns)
    """
    Index(['日付', 'コード', '銘柄名', '市場・商品区分', '33業種コード', '33業種区分', '17業種コード', '17業種区分', '規模コード', '規模区分'], dtype='object')
    """
    list_market = [
        'グロース（内国株式）',
        'グロース（外国株式）',
        'スタンダード（内国株式）',
        'スタンダード（外国株式）',
        'プライム（内国株式）',
        'プライム（外国株式）',
    ]

    df_stock = df[df['市場・商品区分'].isin(list_market)]
    print(df_stock.head())
