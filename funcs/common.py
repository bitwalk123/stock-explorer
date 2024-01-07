import json
import os

import pandas as pd
import wget as wget
from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle


def delete_file(filename: str) -> bool:
    """Delete specified filename
    """
    if os.path.exists(filename):
        os.remove(filename)
        return True
    else:
        return False


def get_excel_from_url(url) -> pd.DataFrame:
    """Get Excel file from specified URL

    Args:
        url(str): Excel file in URL

    Returns:
        pd.DataFrame: pandas dataframe
    """
    # delete temporary file if exists
    basename = os.path.basename(url)
    delete_file(basename)
    # download specified file as temporary file
    filename = wget.download(url)
    # read filename as Excel file
    df_excel = pd.read_excel(filename)
    # delete temporary file
    delete_file(filename)

    return df_excel


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


def read_json(file_json: str) -> dict:
    with open(file_json) as f:
        dict_init = json.load(f)
        return dict_init


def write_json(dict_content: dict, file_json: str) -> bool:
    with open(file_json, 'w') as f:
        json.dump(dict_content, f, indent=2)
        return True
