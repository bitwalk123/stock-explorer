import pandas as pd


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# TABLE contract
def create_table_contract() -> str:
    """Create ticker table
    """
    sql = """
        CREATE TABLE contract(
            id_contract INTEGER PRIMARY KEY AUTOINCREMENT,
            '注文番号' INTEGER,
            '状況' STRING,
            '注文日時' INTEGER,
            '銘柄' STRING,
            '銘柄コード・市場' STRING,
            '売買' STRING,
            '口座' STRING,
            '注文方法' STRING,
            '注文数量[株/口]' INTEGER,
            '約定数量[株/口]' INTEGER,
            '注文単価[円]' STRING,
            '約定単価[円]' REAL,
            '約定代金[円]' INTEGER,
            '手数料[円]' INTEGER
        );
    """
    return sql


def select_id_contract_from_contract_with_order_date(order: int, date: int) -> str:
    sql = """
        SELECT id_contract FROM contract
        WHERE 注文番号=%d AND 注文日時=%d;
    """ % (order, date)
    return sql


def insert_into_contract_values(series: pd.Series) -> str:
    sql = 'INSERT INTO contract VALUES(NULL, %d, %s, %d, %s, %s, %s, %s, %s, %d, %d, %s, %f, %d, %d);' % (
        int(series['注文番号']),
        '\'%s\'' % str(series['状況']),
        int(series['注文日時']),
        '\'%s\'' % str(series['銘柄']),
        '\'%s\'' % str(series['銘柄コード・市場']),
        '\'%s\'' % str(series['売買']),
        '\'%s\'' % str(series['口座']),
        '\'%s\'' % str(series['注文方法']),
        int(series['注文数量[株/口]']),
        int(series['約定数量[株/口]']),
        '\'%s\'' % str(series['注文単価[円]']),
        float(series['約定単価[円]'].replace(',', '')),
        int(series['約定代金[円]'].replace(',', '')),
        int(series['手数料[円]'])
    )
    return sql


def update_contract_values(id_contract: int, series: pd.Series) -> str:
    sql = """
        UPDATE contract
        SET '注文番号'=%d,
            '状況'=%s,
            '注文日時'=%d,
            '銘柄'=%s,
            '銘柄コード・市場'=%s,
            '売買'=%s,
            '口座'=%s,
            '注文方法'=%s,
            '注文数量[株/口]'=%d,
            '約定数量[株/口]'=%d,
            '注文単価[円]'=%s,
            '約定単価[円]'=%f,
            '約定代金[円]'=%d,
            '手数料[円]'=%d
        WHERE id_contract=%d;
    """ % (
        int(series['注文番号']),
        '\'%s\'' % str(series['状況']),
        int(series['注文日時']),
        '\'%s\'' % str(series['銘柄']),
        '\'%s\'' % str(series['銘柄コード・市場']),
        '\'%s\'' % str(series['売買']),
        '\'%s\'' % str(series['口座']),
        '\'%s\'' % str(series['注文方法']),
        int(series['注文数量[株/口]']),
        int(series['約定数量[株/口]']),
        '\'%s\'' % str(series['注文単価[円]']),
        float(series['約定単価[円]'].replace(',', '')),
        int(series['約定代金[円]'].replace(',', '')),
        int(series['手数料[円]']),
        id_contract
    )
    return sql
