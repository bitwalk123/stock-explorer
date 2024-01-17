import datetime as dt
from typing import Union

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QLineEdit


class EntryTicker(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setFrame(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(75)
        self.setStyleSheet('QLineEdit {padding-left:5px;}')


class EntryDate(QLineEdit):
    date = None

    def __init__(self):
        super().__init__()
        self.setFrame(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedWidth(100)
        self.setStyleSheet('QLineEdit {padding-left:5px;}')

    def getDate(self) -> Union[QDate, None]:
        return self.date

    def setDate(self, date: QDate):
        self.date = date
        date_text = str(dt.date(*date.getDate()))
        self.setText(date_text)

    def getDateRange(self) -> tuple:
        start = str(dt.date(*self.date.getDate()))
        date_end = self.date.addDays(1)
        end = str(dt.date(*date_end.getDate()))
        return start, end
