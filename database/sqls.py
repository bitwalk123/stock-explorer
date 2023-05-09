import pandas as pd


def get_sql_create_table_ticker() -> str:
    sql = """
        CREATE TABLE ticker(
            id_ticker INTEGER PRIMARY KEY AUTOINCREMENT,
            '日付' INTEGER,
            'コード' INTEGER,
            '銘柄名' STRING,
            '市場・商品区分' STRING,
            '33業種コード' INTEGER,
            '33業種区分' STRING,
            '17業種コード' INTEGER,
            '17業種区分' STRING,
            '規模コード' STRING,
            '規模区分' STRING
        )
    """
    return sql


def get_sql_drop_table_ticker() -> str:
    sql = 'DROP TABLE IF EXISTS ticker'
    return sql


def get_sql_insert_into_ticker_values(series: pd.Series) -> str:
    sql = 'INSERT INTO ticker VALUES(NULL, %d, %d, "%s", "%s", %d, "%s", %d, "%s", "%s", "%s")' % (
        series['日付'],
        series['コード'],
        series['銘柄名'],
        series['市場・商品区分'],
        series['33業種コード'],
        series['33業種区分'],
        series['17業種コード'],
        series['17業種区分'],
        series['規模コード'],
        series['規模区分']
    )
    return sql
