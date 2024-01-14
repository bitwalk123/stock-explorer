import pandas as pd


def sql_create_tbl_exchange() -> str:
    """Create trade table
    """
    sql = """
        CREATE TABLE exchange
        (
            id_exchange serial,
            id_currency integer,
            "Date" integer,
            "Open" real,
            "High" real,
            "Low" real,
            "Close" real,
            "Adj Close" real,
            PRIMARY KEY (id_exchange)
        );
    """
    return sql


def sql_drop_tbl_exchange() -> str:
    sql = 'DROP TABLE IF EXISTS exchange;'
    return sql


def sql_ins_into_exchange_values(id_currency: int, series: pd.Series) -> str:
    sql = 'INSERT INTO exchange VALUES(default, %d, %d, %f, %f, %f, %f, %f);' % (
        id_currency,
        int(series['Date']),
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close']
    )
    return sql


def sql_sel_all_from_exchange_with_id_currency(id_currency: int) -> str:
    sql = """
        SELECT "Date", "Open", "High", "Low", "Close" FROM exchange
        WHERE id_currency=%d
        ORDER BY "Date" ASC;
    """ % id_currency
    return sql


def sql_sel_all_from_exchange_with_id_currency_start(id_currency: int, start: int) -> str:
    sql = """
        SELECT "Date", "Open", "High", "Low", "Close" FROM exchange
        WHERE id_currency=%d AND "Date" >= %d
        ORDER BY "Date" ASC;
    """ % (id_currency, start)
    return sql


def sql_sel_id_exchange_from_exchange_with_date_id_currency(id_currency: int, timestamp: int) -> str:
    sql = """
        SELECT "id_exchange" FROM exchange
        WHERE "id_currency"=%d AND "Date"=%d;
    """ % (id_currency, timestamp)
    return sql


def sql_sel_max_date_from_exchange_with_id_currency(id_currency: int) -> str:
    sql = """
        SELECT MAX("Date") FROM exchange
        WHERE id_currency=%d;
    """ % id_currency
    return sql


def sql_upd_exchange_values(id_exchange: int, series: pd.Series) -> str:
    sql = """
        UPDATE exchange
        SET "Open"=%f,
            "High"=%f,
            "Low"=%f,
            "Close"=%f,
            "Adj Close"=%f
        WHERE "id_exchange"=%d;
    """ % (
        series['Open'],
        series['High'],
        series['Low'],
        series['Close'],
        series['Adj Close'],
        id_exchange
    )
    return sql
