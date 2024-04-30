import sys

from PySide6.QtWidgets import QApplication

from funcs.tbl_order import create_tbl_order
from snippets.set_env import set_env

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dict_info = set_env()

    # create table order
    result = create_tbl_order()
    print(result)
