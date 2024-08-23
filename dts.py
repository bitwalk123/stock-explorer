import os
import numpy as np
import pandas as pd
import sys

from PySide6.QtCore import Qt, QDate, QDir
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from snippets.set_env import set_env
from structs.res import AppRes
from ui.toolbar_dts import DTSToolBar


class MyTrade:
    def __init__(self):
        self.result = 0

    def update(self, t: pd.Timestamp, price: np.float64):
        print(t, price)


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
        self.toolbar.folderClicked.connect(self.on_open)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    def on_open(self, QStringList=None):
        dialog = QFileDialog()
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            df = pd.read_pickle(filename)
            self.simulation(df)

    def simulation(self, df: pd.DataFrame):
        trade = MyTrade()
        for t in df.index:
            price = df.loc[t]['Price']
            trade.update(t, price)


def main():
    app = QApplication()
    ex = DayTrendSimulator()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
