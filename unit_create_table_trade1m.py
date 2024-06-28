import sys

from PySide6.QtWidgets import QApplication

from funcs.tbl_trade_day import create_tbl_trade1m
from snippets.set_env import set_env

if __name__ == '__main__':
    # This is needed for PySide6 > 6.7
    app = QApplication(sys.argv)

    dict_info = set_env()

    # create trade table
    result = create_tbl_trade1m()
    print(result)
