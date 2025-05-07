import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QTabWidget,
)

from structs.res import AppRes


class StockExplorer(QTabWidget):
    __app_name__ = 'Stock Explorer'
    __version__ = '0.4.0'

    def __init__(self):
        super().__init__()
        self.res = res = AppRes()

        icon = QIcon(os.path.join(res.dir_image, 'stock.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle(self.__app_name__)


def main():
    app = QApplication(sys.argv)
    win = StockExplorer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
