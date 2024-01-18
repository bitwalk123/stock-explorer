import pandas as pd


def sql_create_tbl_trade() -> str:
    """Create trade table
    """
    sql = """
        CREATE TABLE trade
        (
            id_trade serial,
            id_code integer,
            "Date" integer,
            "Open" real,
            "High" real,
            "Low" real,
            "Close" real,
            "Adj Close" real,
            "Volume" integer,
            PRIMARY KEY (id_trade)
        );
    """
    return sql


def sql_drop_tbl_trade() -> str:
    sql = 'DROP TABLE IF EXISTS trade;'
    return sql


def sql_ins_into_trade_values(id_code: int, series: pd.Series) -> str:
    sql = 'INSERT INTO trade VALUES(default, %d, %d, %f, %f, %f, %f, %f, %d);' % (
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


def sql_sel_all_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT "Date", "Open", "High", "Low", "Close", "Volume" FROM trade
        WHERE id_code = %d
        ORDER BY "Date" ASC;
    """ % id_code
    return sql


def sql_sel_all_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Open", "High", "Low", "Close", "Volume" FROM trade
        WHERE id_code = %d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_close_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT "Date", "Close" FROM trade
        WHERE id_code = %d
        ORDER BY "Date" ASC;
    """ % id_code
    return sql


def sql_sel_close_from_trade_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT "Close" FROM trade
        WHERE id_code = %d AND "Date" = %d;
    """ % (id_code, date)
    return sql


def sql_sel_close_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Close" FROM trade
        WHERE id_code = %d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_close_volume_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT "Date", "Close", "Volume" FROM trade
        WHERE id_code = %d
        ORDER BY "Date" ASC;
    """ % id_code
    return sql


def sql_sel_close_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Close", "Volume" FROM trade
        WHERE id_code = %d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_id_trade_from_trade_with_date_id_code(id_code: int, timestamp: int) -> str:
    sql = """
        SELECT "id_trade" FROM trade
        WHERE "id_code" = %d AND "Date" = %d;
    """ % (id_code, timestamp)
    return sql


def sql_sel_max_date_from_trade_less_date(date: int) -> str:
    sql = """
        SELECT MAX("Date") FROM trade
        WHERE "Date" < %d;
    """ % date
    return sql


def sql_sel_max_date_from_trade_with_id_code_less_date(id_code: int, date: int) -> str:
    sql = """
        SELECT MAX("Date") FROM trade
        WHERE id_code = %d AND "Date" < %d;
    """ % (id_code, date)
    return sql


def sql_sel_max_date_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT MAX("Date") FROM trade
        WHERE id_code = %d;
    """ % id_code
    return sql


def sql_sel_open_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT "Date", "Open" FROM trade
        WHERE id_code = %d
        ORDER BY "Date" ASC;
    """ % id_code
    return sql


def sql_sel_open_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Open" FROM trade
        WHERE id_code = %d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_open_volume_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT "Date", "Open", "Volume" FROM trade
        WHERE id_code = %d
        ORDER BY "Date" ASC;
    """ % id_code
    return sql


def sql_sel_open_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Open", "Volume" FROM trade
        WHERE id_code = %d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_open_close_volume_from_trade_with_id_code(id_code: int) -> str:
    sql = """
        SELECT "Date", "Open", "Close", "Volume" FROM trade
        WHERE id_code = %d
        ORDER BY "Date" ASC;
    """ % id_code
    return sql


def sql_sel_open_close_volume_from_trade_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Open", "Close", "Volume" FROM trade
        WHERE id_code = %d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_open_close_from_trade_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT "Open", "Close" FROM trade
        WHERE id_code = %d AND "Date" = %d;
    """ % (id_code, date)
    return sql


def sql_sel_max_date_from_trade() -> str:
    sql = """
        SELECT MAX("Date") FROM trade;
    """
    return sql


def sql_upd_trade_values(id_trade: int, series: pd.Series) -> str:
    sql = """
        UPDATE trade
        SET "Open" = %f,
            "High" = %f,
            "Low" = %f,
            "Close" = %f,
            "Adj Close" = %f,
            "Volume" = %d
        WHERE "id_trade" = %d;
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
