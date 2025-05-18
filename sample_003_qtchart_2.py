import sys

import pandas as pd
from PySide6.QtCore import QTime, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from widgets.toolbar import ToolBarTick
from widgets.views import TickView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.df = pd.DataFrame()
        self.row = 0
        self.length = 0
        self.msec_delta = 9 * 60 * 60 * 1000
        self.resize(1000, 500)

        toolbar = ToolBarTick(res)
        toolbar.fileSelected.connect(self.on_file_selected)
        self.addToolBar(toolbar)

        self.view = view = TickView()
        self.setCentralWidget(view)

        self.timer = timer = QTimer()
        timer.timeout.connect(self.on_update_data)
        timer.setInterval(5)

    def on_file_selected(self, file_excel: str):
        wb = pd.ExcelFile(file_excel)
        sheets = wb.sheet_names
        self.df = wb.parse(sheet_name=sheets[1])
        self.length = len(self.df)

        self.timer.start()

    def on_update_data(self):
        if self.row < self.length:
            t = self.df.iloc[self.row]['Time']
            p = self.df.iloc[self.row]['Price']

            x = QTime.fromString(str(t), 'H:mm:ss').msecsSinceStartOfDay() - self.msec_delta
            y = float(p)
            self.view.appendPoint(x, y)

            self.row += 1
        else:
            self.timer.stop()
            print('Time stopped!')


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
