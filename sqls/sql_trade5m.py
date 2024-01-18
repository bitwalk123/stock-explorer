import pandas as pd


def sql_create_tbl_trade5m() -> str:
    """Create 'trade5m' table
    """
    sql = """
        CREATE TABLE trade5m
        (
            id_trade5m serial,
            id_code integer,
            "Date" integer,
            "Open" real,
            "High" real,
            "Low" real,
            "Close" real,
            "Adj Close" real,
            "Volume" integer,
            PRIMARY KEY (id_trade5m)
        );
    """
    return sql


def sql_drop_tbl_trade5m() -> str:
    sql = 'DROP TABLE IF EXISTS trade5m;'
    return sql


def sql_ins_into_trade5m_values(id_code: int, series: pd.Series) -> str:
    sql = 'INSERT INTO trade5m VALUES(default, %d, %d, %f, %f, %f, %f, %f, %d);' % (
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


def sql_sel_all_from_trade5m_with_dates_id_code_date(id_code: int, start: int) -> str:
    sql = """
        SELECT "Date", "Open", "High", "Low", "Close", "Volume" FROM trade5m
        WHERE id_code = %d AND "Date" = %d
        ORDER BY "Date" ASC;
    """ % (id_code, start)
    return sql


def sql_sel_all_from_trade5m_with_dates_id_code_dates(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT "Date", "Open", "High", "Low", "Close", "Volume" FROM trade5m
        WHERE id_code = %d AND "Date" >= %d AND "Date" < %d
        ORDER BY "Date" ASC;
    """ % (id_code, start, end)
    return sql


def sql_sel_id_trade5m_from_trade5m_with_dates_id_code(id_code: int, start: int, end: int) -> str:
    sql = """
        SELECT "id_trade5m" FROM trade5m
        WHERE "id_code" = %d AND "Date" => %d AND "Date" < %d;
    """ % (id_code, start, end)
    return sql


def sql_upd_trade5m_values(id_trade5m: int, series: pd.Series) -> str:
    sql = """
        UPDATE trade5m
        SET "Open" = %f,
            "High" = %f,
            "Low" = %f,
            "Close" = %f,
            "Adj Close" = %f,
            "Volume" = %d
        WHERE "id_trade5m" = %d;
    """ % (
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close'],
        int(series['Volume']),
        id_trade5m
    )
    return sql
