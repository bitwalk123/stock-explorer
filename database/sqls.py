import pandas as pd


def get_sql_create_table_contract() -> str:
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


def get_sql_update_contract_values(id_contract: int, series: pd.Series) -> str:
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


def get_sql_insert_into_contract_values(series: pd.Series) -> str:
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


def get_sql_select_id_contract_from_contract_with_order_date(order: int, date: int) -> str:
    sql = """
        SELECT id_predict FROM predict
        WHERE '注文番号'=%d AND '注文日時'=%d;
    """ % (order, date)
    return sql


def get_sql_create_table_predict() -> str:
    """Create trade table
    """
    sql = """
        CREATE TABLE predict(
            id_predict INTEGER PRIMARY KEY AUTOINCREMENT,
            id_code INTEGER,
            date INTEGER,
            comp INTEGER,
            rmse REAL,
            r2 REAL,
            open REAL
        );
    """
    return sql


def get_sql_insert_into_predict_values(id_code: int, date: int, series: pd.Series) -> str:
    sql = 'INSERT INTO predict VALUES(NULL, %d, %d, %d, %f, %f, %f);' % (
        id_code,
        date,
        int(series['Components']),
        series['RMSE'],
        series['R2'],
        series['Open']
    )
    return sql


def get_sql_select_id_predict_from_predict_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT id_predict FROM predict
        WHERE id_code=%d AND date=%d;
    """ % (id_code, date)
    return sql


def get_sql_update_predict_values(id_predict: int, series: pd.Series) -> str:
    sql = """
        UPDATE predict
        SET comp=%f,
            rmse=%f,
            r2=%f,
            open=%f
        WHERE id_predict=%d;
    """ % (
        int(series['Components']),
        series['RMSE'],
        series['R2'],
        series['Open'],
        id_predict
    )
    return sql


def get_sql_create_table_split() -> str:
    """Create trade table
    """
    sql = """
        CREATE TABLE split(
            id_split INTEGER PRIMARY KEY AUTOINCREMENT,
            id_code INTEGER,
            date INTEGER,
            ratio REAL
        );
    """
    return sql


def get_sql_create_table_ticker() -> str:
    """Create ticker table
    """
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
        );
    """
    return sql


def get_sql_create_table_trade() -> str:
    """Create trade table
    """
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
        );
    """
    return sql


def get_sql_delete_trade_with_id_trade(id_trade: int) -> str:
    """Delete record of trade table with specified id_trade

    Args:
        id_trade(int): id_trade
    """
    sql = 'DELETE FROM trade WHERE id_trade = %d;' % id_trade
    return sql


def get_sql_drop_table_ticker() -> str:
    """Drop table ticker if exists
    """
    sql = 'DROP TABLE IF EXISTS ticker;'
    return sql


def get_sql_insert_into_ticker_values(series: pd.Series) -> str:
    sql = 'INSERT INTO ticker VALUES(NULL, %d, %d, "%s", "%s", %d, "%s", %d, "%s", "%s", "%s");' % (
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


def get_sql_insert_into_split_values() -> str:
    sql = 'INSERT INTO split VALUES(NULL, ?, ?, ?);'
    return sql


def get_sql_insert_into_trade_values(id_code: int, series: pd.Series) -> str:
    sql = 'INSERT INTO trade VALUES(NULL, %d, %d, %f, %f, %f, %f, %f, %d);' % (
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


def get_sql_select_all_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date, open, high, low, close, volume FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def get_sql_select_all_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, open, high, low, close, volume FROM trade
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def get_sql_select_code_cname_from_ticker() -> str:
    sql = 'select コード, 銘柄名 from ticker;'
    return sql


def get_sql_select_code_from_ticker() -> str:
    sql = 'SELECT コード FROM ticker;'
    return sql


def get_sql_select_count_from_ticker() -> str:
    sql = 'SELECT COUNT(*) FROM ticker;'
    return sql


def get_sql_select_dataset_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT date, open, high, low, close FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d;
    """ % (id_code, start, end)
    return sql


def get_sql_select_date_from_split_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date FROM split
        WHERE id_code=%d;
    """ % id_code
    return sql


def get_sql_select_date_id_code_from_ticker(date: int, id_code: int) -> str:
    sql = """
        SELECT date, id_code FROM trade
        WHERE date=%d AND id_code=%d;
    """ % (date, id_code)
    return sql


def get_sql_select_date_open_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date, open FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def get_sql_select_date_open_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT date, open FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d
        ORDER BY date;
    """ % (id_code, start, end)
    return sql


def get_sql_select_date_open_volume_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date, open, volume FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def get_sql_select_date_open_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, open, volume FROM trade
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def get_sql_select_date_ratio_with_id_code(id_code: int):
    sql = """
        SELECT id_split, date, ratio from split
        WHERE id_code=%d;
    """ % id_code
    return sql


def get_sql_select_date_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, volume FROM trade
        WHERE id_code=%d AND date >= %d;
    """ % (id_code, start)
    return sql


def get_sql_select_id_code_from_predict() -> str:
    sql = """
        SELECT id_code FROM predict;
    """
    return sql


def get_sql_select_id_code_from_ticker() -> str:
    sql = """
        SELECT id_code FROM ticker;
    """
    return sql


def get_sql_select_id_code_code_from_ticker() -> str:
    sql = """
        SELECT id_code, コード FROM ticker;
    """
    return sql


def get_sql_select_id_code_code_cname_from_ticker() -> str:
    sql = """
        SELECT id_code, コード, 銘柄名 FROM ticker;
    """
    return sql


def get_sql_select_id_code_cname_from_ticker_with_code(code: int) -> str:
    sql = """
        SELECT id_code, 銘柄名 FROM ticker
        WHERE コード=%d;
    """ % code
    return sql


def get_sql_select_id_code_from_ticker_with_code(code: int) -> str:
    sql = """
        SELECT id_code FROM ticker
        WHERE コード=%d;
    """ % code
    return sql


def get_sql_select_id_trade_date_open_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT id_trade, date, open FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def get_sql_select_id_trade_date_open_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT id_trade, date, open FROM trade
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def get_sql_select_id_trade_from_trade_with_date_id_code(date: int, id_code: int) -> str:
    sql = """
        SELECT id_trade FROM trade
        WHERE date=%d AND id_code=%d;
    """ % (date, id_code)
    return sql


def get_sql_select_max_date_from_trade() -> str:
    sql = "SELECT MAX(date) FROM trade;"
    return sql


def get_sql_select_max_date_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT MAX(date) FROM trade
        WHERE id_code=%d;
    """ % id_code
    return sql


def get_sql_select_max_date_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT MAX(date) FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d;
    """ % (id_code, start, end)
    return sql


def get_sql_select_min_date_from_trade_with_id_code_end(id_code: int, end: int) -> str:
    """This SQL searches next trade day from end date specified"""
    sql = """
        SELECT MIN(date) FROM trade
        WHERE id_code=%d AND date > %d;
    """ % (id_code, end)
    return sql


def get_sql_select_open_from_trade_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT open FROM trade
        WHERE id_code=%d AND date = %d;
    """ % (id_code, date)
    return sql


def get_sql_select_open_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT open FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d;
    """ % (id_code, start, end)
    return sql


def get_sql_select_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT volume FROM trade
        WHERE id_code=%d AND date >= %d;
    """ % (id_code, start)
    return sql


def get_sql_select_volume_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT volume FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d;
    """ % (id_code, start, end)
    return sql


def get_sql_update_trade_values(id_trade: int, series: pd.Series) -> str:
    sql = """
        UPDATE trade
        SET open=%f,
            high=%f,
            low=%f,
            close=%f,
            close_adj=%f,
            volume=%d
        WHERE id_trade=%d;
    """ % (
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close'],
        int(series['Volume']),
        id_trade
    )
    return sql
