import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QApplication

from structs.res import AppRes


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), 'trends.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('Day Trend Analyzer (widh DB), DTA')
        self.setMinimumSize(1000, 700)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
