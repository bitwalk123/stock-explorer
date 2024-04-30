import sys

from PySide6.QtWidgets import QApplication

from funcs.tbl_itrade import (
    create_tbl_itrade,
    init_tbl_itrade,
)
from snippets.set_env import set_env

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dict_info = set_env()

    # create itrade table
    result = create_tbl_itrade()
    print(result)

    # initialize itrade table
    result = init_tbl_itrade()
    print(result)
