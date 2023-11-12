#!/usr/bin/env python
# coding: utf-8
import datetime
import os
import re
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
)

from functions.get_dict_code import get_dict_code_cname
from functions.resources import get_connection
from widgets.worksheet import WorkSheet


class TransactionManager(QMainWindow):
    """Main class for this application
    """
    __version__ = '0.0.1'
    pattern_date = re.compile(r'^(\d{1,2})/(\d{1,2})$')

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Transaction Manager')
        self.dict_cname = get_dict_code_cname()
        print(self.dict_cname)
        self.headers = ['取引日', 'コード', '銘柄', '株数', '買値', '売値', '損益', 'コメント', 'コメント２']
        self.sheet = WorkSheet(col_max=len(self.headers))
        self.init_ui()

        icon = QIcon(os.path.join('images', 'spreadsheet.png'))
        self.setWindowIcon(icon)
        self.resize(800, 600)

    def init_ui(self):
        self.sheet.setHorizontalHeaderLabels(self.headers)
        self.sheet.cellUpdated.connect(self.cell_updated)
        self.setCentralWidget(self.sheet)

    def cell_updated(self, item: QTableWidgetItem):
        self.sheet.disableEvent()
        row = item.row()
        col = item.column()
        value = item.text()

        header = self.headers[col]
        if header == '取引日':
            value_date = ''
            if value == 'today':
                value_date = self.get_today_str()
            else:
                m = self.pattern_date.match(value)
                if m:
                    value_date = self.get_date_str(m)
            item.setText(value_date)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        elif header == 'コード':
            value_new = ''
            if self.is_num(value):
                value_new = str(int(float(value)))
                if value_new in self.dict_cname.keys():
                    self.set_cname(row, value_new)
            item.setText(value_new)
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)

        self.sheet.enableEvent()

    @staticmethod
    def get_date_str(m: re.Match) -> str:
        month = int(m.group(1))
        day = int(m.group(2))
        dt_now = datetime.datetime.now()
        year = dt_now.year
        value_date = '%4d/%02d/%02d' % (year, month, day)
        return value_date

    @staticmethod
    def get_today_str():
        dt_now = datetime.datetime.now()
        year = dt_now.year
        month = dt_now.month
        day = dt_now.day
        value_date = '%4d/%02d/%02d' % (year, month, day)
        return value_date

    @staticmethod
    def is_num(str_float: str) -> bool:
        try:
            float(str_float)
        except ValueError:
            return False
        else:
            return True

    def set_cname(self, row: int, code_str: str):
        col_cname = self.headers.index('銘柄')
        item_cname = self.sheet.item(row, col_cname)
        if item_cname is None:
            item_cname = QTableWidgetItem()
            self.sheet.setItem(row, col_cname, item_cname)
        item_cname.setText(self.dict_cname[code_str])
        item_cname.setTextAlignment(Qt.AlignmentFlag.AlignLeft)


def main():
    app = QApplication(sys.argv)
    obj = TransactionManager()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
