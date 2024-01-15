import pandas as pd


def sql_create_tbl_ticker() -> str:
    sql = '''
        CREATE TABLE IF NOT EXISTS ticker
        (
            id_code serial,
            "日付" integer,
            "コード" character varying(4) UNIQUE,
            "銘柄名" character varying(255),
            "市場・商品区分" character varying(255),
            "33業種コード" integer,
            "33業種区分" character varying(255),
            "17業種コード" integer,
            "17業種区分" character varying(255),
            "規模コード" character varying(255),
            "規模区分" character varying(255),
            PRIMARY KEY (id_code)
        )
    '''
    return sql


def sql_del_ticker_with_code(code: str) -> str:
    sql = """
        DELETE FROM ticker WHERE "コード"='%s';
    """ % code
    return sql


def sql_drop_tbl_ticker() -> str:
    sql = 'DROP TABLE IF EXISTS ticker;'
    return sql


def sql_ins_into_ticker_vals(series: pd.Series) -> str:
    sql = """
        INSERT INTO ticker
        VALUES(
            default, %d, %s, '%s', '%s', %d, '%s', %d, '%s', '%s', '%s'
        );
    """ % (
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


def sql_sel_13sector_from_ticker():
    sql = """
        SELECT "33業種区分" FROM ticker;
    """
    return sql


def sql_sel_13sector_from_ticker_with_code(code: str):
    sql = """
        SELECT "33業種区分" FROM ticker
        WHERE "コード" = '%s';
    """ % code
    return sql


def sql_sel_cname_with_code_from_ticker(code: str) -> str:
    sql = """
        SELECT "銘柄名" FROM ticker
        WHERE "コード"='%s';
    """ % code
    return sql


def sql_sel_code_from_ticker() -> str:
    sql = """
        SELECT "コード" FROM ticker
        ORDER BY "コード" ASC;
    """
    return sql


def sql_sel_id_code_code_from_ticker() -> str:
    sql = """
        SELECT id_code, "コード" FROM ticker
        ORDER BY "コード" ASC;
    """
    return sql


def sql_sel_id_code_cname_from_ticker_with_code(code: str) -> str:
    sql = """
        SELECT id_code, "銘柄名" FROM ticker
        WHERE "コード"='%s';
    """ % code
    return sql


def sql_sel_id_code_from_ticker_with_code(code: str) -> str:
    sql = """
        SELECT id_code FROM ticker
        WHERE "コード"='%s';
    """ % code
    return sql


def sql_upd_ticker_vals(id_code: int, series: pd.Series) -> str:
    sql = """
        UPDATE ticker
        SET "日付"=%d,
            "コード"='%s',
            "銘柄名"='%s',
            "市場・商品区分"='%s',
            "33業種コード"=%d,
            "33業種区分"='%s',
            "17業種コード"=%d,
            "17業種区分"='%s',
            "規模コード"='%s',
            "規模区分"='%s'
        WHERE id_code=%d;
    """ % (
        series['日付'],
        series['コード'],
        series['銘柄名'],
        series['市場・商品区分'],
        series['33業種コード'],
        series['33業種区分'],
        series['17業種コード'],
        series['17業種区分'],
        series['規模コード'],
        series['規模区分'],
        id_code,
    )
    return sql
