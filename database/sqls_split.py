# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# TABLE split
def create_table_split() -> str:
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


def insert_into_split_values() -> str:
    sql = 'INSERT INTO split VALUES(NULL, ?, ?, ?);'
    return sql


def select_date_from_split_with_id_code(id_code: int) -> str:
    sql = """
        SELECT date FROM split
        WHERE id_code=%d;
    """ % id_code
    return sql


def select_date_ratio_from_split_with_id_code(id_code: int):
    sql = """
        SELECT id_split, date, ratio from split
        WHERE id_code=%d;
    """ % id_code
    return sql
