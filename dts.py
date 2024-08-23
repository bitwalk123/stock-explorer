import os
import pandas as pd
import sys

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from funcs.dta_funcs import dta_get_data_from_dbrt
from funcs.tbl_ticker import get_dict_id_code
from funcs.tide import get_day_timestamp
from snippets.set_env import set_env
from structs.res import AppRes
from ui.toolbar_dts import DTSToolBar


class DayTrendSimulator(QMainWindow):
    app_ver = '0.0.1'

    def __init__(self):
        super().__init__()
        dict_info = set_env()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'simulator.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Simulator, DTS')

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTSToolBar()
        self.toolbar.folderClicked.connect(self.open_file)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def open_file(self):
        print('DEBUG!')


def main():
    app = QApplication()
    ex = DayTrendSimulator()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
