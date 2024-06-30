import os
import pandas as pd
import sys

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from structs.res import AppRes
from ui.toolbar_dta import DTAToolBarPlus


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (widh DB), DTA')
        self.setMinimumSize(1000, 700)

        # _____________________________________________________________________
        # Toolbar
        self.toolbar = toolbar = DTAToolBarPlus()
        toolbar.clickedPlot.connect(self.on_plot)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def getTimeStamp(self, qdate) -> pd.Timestamp:
        date_str = '%s-%s-%s 00:00:00+09:00' % (qdate.year(), qdate.month(), qdate.day())
        return pd.to_datetime(date_str)

    def on_plot(self, qdate: QDate):
        d1 = self.getTimeStamp(qdate)
        d2 = self.getTimeStamp(qdate.addDays(1))
        print(d1, d2)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
