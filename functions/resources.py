import os
import platform
from os.path import expanduser

import pandas as pd
import wget
from PySide6.QtCore import QObject, QThreadPool
from PySide6.QtGui import QIcon
from PySide6.QtSql import QSqlDatabase
from PySide6.QtWidgets import QStyle
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
    """
    dbname = get_info('db')
    if flag_delete:
        delete_file(dbname)

    con.setDatabaseName(dbname)
    return con


def get_info(key: str) -> str:
    """Get key value of resource dictionary
    """
    return res[key]


def get_ini_file() -> str:
    """Get name of ini file
    """
    # Name of ini file depends on OS.
    if platform.system() == 'Windows':
        file_config = 'stock_explorer.ini'
    else:
        file_config = '.stock_explorer'
    # ini file in full path
    return os.path.join(expanduser('~'), file_config)


def get_standard_icon(parent: QObject, name_pixmap: str) -> QIcon:
    """Get Standard Pixmap and convert QIcon instance

    Args:
        parent(QObject): Parent instance inheriting from the QObject.
        name_pixmap(str): name of standard picmap

    Returns:
        QIcon: instance of QIcon of specified pixmap
    """
    pixmap = getattr(QStyle.StandardPixmap, name_pixmap)
    icon = parent.style().standardIcon(pixmap)

    return icon


def get_threadpool() -> QThreadPool:
    """Get thread pool instance
    """
    return threadpool


def get_tse_data():
    """Get TSE data in Excel format from specified URL
    """
    url = get_info('tse')
    basename = os.path.basename(url)
    delete_file(basename)
    filename = wget.download(url)
    df_all = pd.read_excel(filename)
    delete_file(filename)
    return df_all
