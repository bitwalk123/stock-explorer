import pandas as pd


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# TABLE trade
def create_table_trade() -> str:
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


def delete_trade_with_id_trade(id_trade: int) -> str:
    """Delete record of trade table with specified id_trade

    Args:
        id_trade(int): id_trade
    """
    sql = 'DELETE FROM trade WHERE id_trade = %d;' % id_trade
    return sql


def insert_into_trade_values(id_code: int, series: pd.Series) -> str:
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


def select_all_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date, open, high, low, close, volume FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def select_all_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, open, high, low, close, volume FROM trade
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def select_close_from_trade_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT close FROM trade
        WHERE id_code=%d AND date = %d;
    """ % (id_code, date)
    return sql


def select_dataset_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT date, open, high, low, close FROM trade
        WHERE id_code=%d AND date > %d AND date <= %d;
    """ % (id_code, start, end)
    return sql


def select_date_from_trade() -> str:
    sql = "SELECT date FROM trade ORDER BY date;"
    return sql


def select_date_open_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date, open FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def select_date_open_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT date, open FROM trade
        WHERE id_code=%d AND date >= %d AND date <= %d
        ORDER BY date;
    """ % (id_code, start, end)
    return sql


def select_date_open_volume_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date, open, volume FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def select_date_open_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, open, volume FROM trade
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def select_date_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, volume FROM trade
        WHERE id_code=%d AND date >= %d;
    """ % (id_code, start)
    return sql


def select_id_trade_date_open_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT id_trade, date, open FROM trade
        WHERE id_code=%d
        ORDER BY date;
    """ % id_code
    return sql


def select_id_trade_date_open_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT id_trade, date, open FROM trade
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def select_id_trade_from_trade_with_date_id_code(date: int, id_code: int) -> str:
    sql = """
        SELECT id_trade FROM trade
        WHERE date=%d AND id_code=%d;
    """ % (date, id_code)
    return sql


def select_max_date_from_trade() -> str:
    sql = "SELECT MAX(date) FROM trade;"
    return sql


def select_max_date_from_trade_less_date(date: int) -> str:
    sql = """
        SELECT MAX(date) FROM trade
        WHERE date < %d;
    """ % date
    return sql


def select_max_date_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT MAX(date) FROM trade
        WHERE id_code=%d;
    """ % id_code
    return sql


def select_max_date_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT MAX(date) FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d;
    """ % (id_code, start, end)
    return sql


def select_min_date_from_trade_with_id_code_end(id_code: int, end: int) -> str:
    """This SQL searches next trade day from end date specified"""
    sql = """
        SELECT MIN(date) FROM trade
        WHERE id_code=%d AND date > %d;
    """ % (id_code, end)
    return sql


def select_open_from_trade_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT open FROM trade
        WHERE id_code=%d AND date = %d;
    """ % (id_code, date)
    return sql


def select_open_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT open FROM trade
        WHERE id_code=%d AND date >= %d AND date <= %d;
    """ % (id_code, start, end)
    return sql


def select_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT volume FROM trade
        WHERE id_code=%d AND date >= %d;
    """ % (id_code, start)
    return sql


def select_volume_from_trade_with_id_code_start_end(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT volume FROM trade
        WHERE id_code=%d AND date >= %d AND date < %d;
    """ % (id_code, start, end)
    return sql


def update_trade_values(id_trade: int, series: pd.Series) -> str:
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
