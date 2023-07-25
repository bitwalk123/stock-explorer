import pandas as pd


def get_sql_create_table_ticker() -> str:
    sql = """
        CREATE TABLE ticker(
            id_code INTEGER PRIMARY KEY AUTOINCREMENT,
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


def get_sql_create_table_trade() -> str:
    sql = """
        CREATE TABLE trade(
            id_trade INTEGER PRIMARY KEY AUTOINCREMENT,
            id_code INTEGER,
            date INTEGER,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            close_adj REAL,
            volume INTEGER
        )
    """
    return sql


def get_sql_delete_trade_with_id_trade(id_trade) -> str:
    sql = 'DELETE FROM trade WHERE id_trade = %d' % id_trade
    return sql


def get_sql_drop_table_ticker() -> str:
    """
    drop table ticker if exists
    """
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


def get_sql_insert_into_trade_values(id_code: int, series: pd.Series) -> str:
    sql = 'INSERT INTO trade VALUES(NULL, %d, %d, %f, %f, %f, %f, %f, %d)' % (
        id_code,
        int(series['Date']),
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close'],
        int(series['Volume'])
    )
    return sql


def get_sql_select_code_cname_from_ticker() -> str:
    sql = 'select コード, 銘柄名 from ticker;'
    return sql


def get_sql_select_code_from_ticker() -> str:
    sql = 'SELECT コード FROM ticker;'
    return sql


def get_sql_select_id_code_from_ticker() -> str:
    sql = 'SELECT id_code FROM ticker;'
    return sql


def get_sql_select_id_code_code_from_ticker() -> str:
    sql = 'SELECT id_code, コード FROM ticker;'
    return sql


def get_sql_select_id_code_code_cname_from_ticker() -> str:
    sql = 'SELECT id_code, コード, 銘柄名 FROM ticker;'
    return sql


def get_sql_select_id_code_cname_from_ticker_with_code(code) -> str:
    sql = 'SELECT id_code, 銘柄名 FROM ticker WHERE コード=%d;' % code
    return sql


def get_sql_select_date_open_from_trade_with_id_code(id_code) -> str:
    sql = 'SELECT date, open FROM trade WHERE id_code=%d ORDER BY date;' % id_code
    return sql


def get_sql_select_date_open_from_trade_with_id_code_start(id_code, start) -> str:
    sql = 'SELECT date, open FROM trade WHERE id_code=%d AND date >= %d ORDER BY date;' % (id_code, start)
    return sql


def get_sql_select_max_date_from_trade_with_id_code(id_code: int) -> str:
    sql = 'SELECT MAX(date) FROM trade WHERE id_code=%d;' % id_code
    return sql


def get_sql_select_id_trade_date_open_from_trade_with_id_code(id_code) -> str:
    sql = 'SELECT id_trade, date, open FROM trade WHERE id_code=%d ORDER BY date;' % id_code
    return sql


def get_sql_select_id_trade_date_open_from_trade_with_id_code_start(id_code, start) -> str:
    sql = 'SELECT id_trade, date, open FROM trade WHERE id_code=%d AND date >= %d ORDER BY date;' % (id_code, start)
    return sql
