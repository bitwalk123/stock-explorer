import pandas as pd


def sql_create_tbl_itrade() -> str:
    """Create itrade table
    """
    sql = """
        CREATE TABLE itrade
        (
            id_itrade serial,
            id_index integer,
            "Date" integer,
            "Open" real,
            "High" real,
            "Low" real,
            "Close" real,
            "Adj Close" real,
            "Volume" bigint,
            PRIMARY KEY (id_itrade)
        );
    """
    return sql


def sql_drop_tbl_itrade() -> str:
    sql = 'DROP TABLE IF EXISTS itrade;'
    return sql


def sql_ins_into_itrade_values(id_index: int, series: pd.Series) -> str:
    sql = 'INSERT INTO itrade VALUES(default, %d, %d, %f, %f, %f, %f, %f, %d);' % (
        id_index,
        int(series['Date']),
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close'],
        int(series['Volume'])
    )
    return sql


def sql_sel_id_itrade_from_itrade_with_date_id_index(id_index: int, timestamp: int) -> str:
    sql = """
        SELECT "id_itrade" FROM itrade
        WHERE "id_index"=%d AND "Date"=%d;
    """ % (id_index, timestamp)
    return sql


def sql_sel_max_date_from_itrade_with_id_index(id_index: int) -> str:
    sql = """
        SELECT MAX("Date") FROM itrade
        WHERE id_index = %d;
    """ % id_index
    return sql


def sql_upd_itrade_values(id_itrade: int, series: pd.Series) -> str:
    sql = """
        UPDATE itrade
        SET "Open"=%f,
            "High"=%f,
            "Low"=%f,
            "Close"=%f,
            "Adj Close"=%f,
            "Volume"=%d
        WHERE "id_itrade"=%d;
    """ % (
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close'],
        int(series['Volume']),
        id_itrade
    )
    return sql
