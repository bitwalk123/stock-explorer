import datetime as dt
import pandas as pd

from database.sqls import get_sql_insert_into_contract_values, get_sql_update_contract_values


def main(filename: str):
    columns = [
        '注文番号',
        '状況',
        '注文日時',
        '銘柄',
        '銘柄コード・市場',
        '売買',
        '口座',
        '注文方法',
        '注文数量[株/口]',
        '約定数量[株/口]',
        '注文単価[円]',
        '約定単価[円]',
        '約定代金[円]',
        '手数料[円]'
    ]
    df = pd.read_csv(filename, encoding='shift_jis')
    df2 = df[columns][df['状況'] == '約定']

    y = '2023'
    fmt = '%Y/%m/%d %H:%M'
    col = '注文日時'
    df2[col] = [int(dt.datetime.timestamp(dt.datetime.strptime('%s/%s' % (y, t), fmt))) for t in df2[col]]
    for row_index in df2.index:
        series = df2.loc[row_index]
        sql = get_sql_update_contract_values(0, series)
        print(sql)
        sql = get_sql_insert_into_contract_values(series)
        print(sql)
    df2.to_csv('out.csv', index=False)


if __name__ == '__main__':
    csvname = '/home/bitwalk/ダウンロード/stockorder(JP)_20231026.csv'
    main(csvname)
