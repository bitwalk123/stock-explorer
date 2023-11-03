import os
import datetime as dt

import pandas as pd
import wget
from PySide6.QtCore import QThreadPool
from PySide6.QtSql import QSqlDatabase
from functions.handle_file import delete_file

con = QSqlDatabase.addDatabase('QSQLITE')
threadpool = QThreadPool()

res = {
    'db': 'stock-explorer.sqlite3',
    'tse': 'https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls',
}


def get_con() -> QSqlDatabase:
    """Get instance of database connection
    """
    return con


def get_connection(flag_delete=False) -> QSqlDatabase:
    """Get new database connection

    Args:
        flag_delete(bool): delete the db if True

    Returns:
        QSqlDatabase: instance of QSqlDatabase
    """
    dbname = get_info('db')
    if flag_delete:
        delete_file(dbname)

    con.setDatabaseName(dbname)

    return con


def get_info(key: str) -> str:
    """Get key value of resource dictionary

    Args:
        key(str): keyword of resource dictionary

    Returns:
        str: string value corrensponding to the keyword
    """
    return res[key]


def get_original_start() -> int:
    return int(dt.datetime(2021, 1, 1, 0, 0).timestamp())


def get_threadpool() -> QThreadPool:
    """Get thread pool instance
    """
    return threadpool


def get_tse_data() -> pd.DataFrame:
    """Get TSE data in Excel format from specified URL

    Returns:
        pd.DataFrame: pandas dataframe
    """
    url = get_info('tse')
    basename = os.path.basename(url)
    delete_file(basename)
    filename = wget.download(url)
    df_all = pd.read_excel(filename)
    delete_file(filename)

    return df_all
