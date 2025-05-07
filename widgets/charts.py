import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure

from funcs.plots import (
    clearAxes,
    drawGrid,
    refreshDraw,
)
from structs.res import AppRes


class Canvas(FigureCanvas):
    def __init__(self, res: AppRes):
        self.fig = Figure()
        super().__init__(self.fig)

        font = os.path.join(res.dir_font, 'RictyDiminished-Regular.ttf')
        fm.fontManager.addfont(font)
        font_prop = fm.FontProperties(fname=font)
        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        self.ax = dict()
        n = 2

        if n > 1:
            gs = self.fig.add_gridspec(
                n, 1,
                wspace=0.0, hspace=0.0,
                height_ratios=[3 if i == 0 else 1 for i in range(n)]
            )
            for i, axis in enumerate(gs.subplots(sharex='col')):
                self.ax[i] = axis
        else:
            self.ax[0] = self.fig.add_subplot(111)

        self.fig.subplots_adjust(left=0.07, right=0.98, top=0.92, bottom=0.06)

    def plot(self, dict_plot: dict):
        """
        プロット
        :param dict_plot:
        """

        # 消去
        clearAxes(self.fig)

        # グリッド線
        drawGrid(self.fig)

        # 再描画
        refreshDraw(self.fig)

    def save(self, filename):
        self.fig.savefig(filename)


class ChartNavigation(NavigationToolbar):
    def __init__(self, chart: FigureCanvas):
        super().__init__(chart)
