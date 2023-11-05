import pandas as pd


# _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_
# TABLE predict
def create_table_predict() -> str:
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


def insert_into_predict_values(id_code: int, date: int, series: pd.Series) -> str:
    sql = 'INSERT INTO predict VALUES(NULL, %d, %d, %d, %f, %f, %f);' % (
        id_code,
        date,
        int(series['Components']),
        series['RMSE'],
        series['R2'],
        series['Open']
    )
    return sql


def select_date_open_from_predict_with_id_code_start(id_code: int, start: int) -> str:
    sql = """
        SELECT date, open FROM predict
        WHERE id_code=%d AND date >= %d
        ORDER BY date;
    """ % (id_code, start)
    return sql


def select_id_code_from_predict() -> str:
    sql = """
        SELECT id_code FROM predict;
    """
    return sql


def select_id_predict_from_predict_with_id_code_date(id_code: int, date: int) -> str:
    sql = """
        SELECT id_predict FROM predict
        WHERE id_code=%d AND date=%d;
    """ % (id_code, date)
    return sql


def select_max_date_from_predict() -> str:
    sql = 'SELECT MAX(date) FROM predict;'
    return sql


def update_predict_values(id_predict: int, series: pd.Series) -> str:
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
