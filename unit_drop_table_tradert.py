import sys

from PySide6.QtWidgets import QApplication

from funcs.tbl_trade_day import drop_tbl_tradert
from snippets.set_env import set_env

if __name__ == '__main__':
    # This is needed for PySide6 > 6.7
    app = QApplication(sys.argv)

    dict_info = set_env()
    result = drop_tbl_tradert()
    print(result)
