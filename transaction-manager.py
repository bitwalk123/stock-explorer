#!/usr/bin/env python
# coding: utf-8
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableView,
)


class TransactionManager(QMainWindow):
    """Main class for this application
    """
    __version__ = '0.0.1'

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Transaction Manager')
        icon = QIcon(os.path.join('images', 'spreadsheet.png'))
        self.setWindowIcon(icon)

        self.init_ui()

    def init_ui(self):
        view = QTableView()
        self.setCentralWidget(view)

def main():
    app = QApplication(sys.argv)
    obj = TransactionManager()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
