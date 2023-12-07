import pandas as pd


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# TABLE ticker
def create_table_ticker() -> str:
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


def delete_ticker_with_code(code: int) -> str:
    """Delete record of ticker table with specified code

    Args:
        code(int): ticker code
    """
    sql = 'DELETE FROM ticker WHERE コード=%d;' % code
    return sql


def drop_table_ticker() -> str:
    """Drop table ticker if exists
    """
    sql = 'DROP TABLE IF EXISTS ticker;'
    return sql


def insert_into_ticker_values(series: pd.Series) -> str:
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


def select_13sector_from_ticker_with_code(code: int):
    sql = """
        SELECT "33業種区分" FROM ticker
        WHERE コード=%d;
    """ % code
    return sql


def select_code_cname_from_ticker() -> str:
    sql = """
        SELECT コード, 銘柄名 FROM ticker
        ORDER BY コード;
    """
    return sql


def select_code_from_ticker() -> str:
    sql = """
        SELECT コード FROM ticker
        ORDER BY コード;
    """
    return sql


def select_count_from_ticker() -> str:
    sql = 'SELECT COUNT(*) FROM ticker;'
    return sql


def select_date_id_code_from_ticker(date: int, id_code: int) -> str:
    sql = """
        SELECT date, id_code FROM ticker
        WHERE date=%d AND id_code=%d;
    """ % (date, id_code)
    return sql


def select_id_code_from_ticker() -> str:
    sql = """
        SELECT id_code FROM ticker
        ORDER BY コード;
    """
    return sql


def select_id_code_code_from_ticker() -> str:
    sql = """
        SELECT id_code, コード FROM ticker
        ORDER BY コード;
    """
    return sql


def select_id_code_code_cname_from_ticker() -> str:
    sql = """
        SELECT id_code, コード, 銘柄名 FROM ticker
        ORDER BY コード;
    """
    return sql


def select_id_code_cname_from_ticker_with_code(code: int) -> str:
    sql = """
        SELECT id_code, 銘柄名 FROM ticker
        WHERE コード=%d;
    """ % code
    return sql


def select_id_code_from_ticker_with_code(code: int) -> str:
    sql = """
        SELECT id_code FROM ticker
        WHERE コード=%d;
    """ % code
    return sql


def update_ticker_values(id_code: int, series: pd.Series) -> str:
    sql = """
        UPDATE ticker
        SET 日付=%d,
            コード=%d,
            銘柄名=\"%s\"
        WHERE id_code=%d;
    """ % (
        series['日付'],
        series['コード'],
        series['銘柄名'],
        id_code,
    )
    return sql
