import sys

from PySide6.QtWidgets import QApplication

from funcs.tbl_trade_day import drop_tbl_trade5m
from snippets.set_env import set_env

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dict_info = set_env()
    result = drop_tbl_trade5m()
    print(result)
