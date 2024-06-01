import sys
import datetime
import matplotlib.pyplot as plt
from matplotlib import dates
import numpy as np
import pandas as pd
import scipy.stats
from scipy.interpolate import make_smoothing_spline

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStatusBar, QFileDialog,
)

from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar

from ui.dta import DTAToolBar
from widgets.charts import ChartForAnalysis


class DayTrendAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DayTrendAnalyzer')
        self.setMinimumSize(1000, 400)

        # _____________________________________________________________________
        # Toolbar
        toolbar = DTAToolBar()
        toolbar.clickedOpen.connect(self.on_open)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # _____________________________________________________________________
        # Chart
        chart = ChartForAnalysis()
        self.setCentralWidget(chart)

        # _____________________________________________________________________
        # Navigation Toolbar at Bottom
        navbar = NavigationToolbar(chart, self)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, navbar)

        # _____________________________________________________________________
        # StatusBar
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

    def on_open(self):
        dialog = QFileDialog()
        if dialog.exec():
            filename = dialog.selectedFiles()[0]
            print(filename)


def main():
    app = QApplication()
    ex = DayTrendAnalyzer()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
