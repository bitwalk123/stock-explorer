import sys

import pandas as pd
from PySide6.QtCore import QTime
from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from widgets.toolbar import ToolBarTick
from widgets.views import TickView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.resize(1000, 500)

        toolbar = ToolBarTick(res)
        toolbar.fileSelected.connect(self.on_file_selected)
        self.addToolBar(toolbar)

        self.view = view = TickView()
        self.setCentralWidget(view)

    def on_file_selected(self, file_excel: str):
        wb = pd.ExcelFile(file_excel)
        sheets = wb.sheet_names
        df = wb.parse(sheet_name=sheets[1])
        msec_delta = 9 * 60 * 60 * 1000
        for t, p in zip(df['Time'], df['Price']):
            x = QTime.fromString('%s' % t, 'H:mm:ss').msecsSinceStartOfDay() - msec_delta
            y = float(p)
            self.view.appendPoint(x, y)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
