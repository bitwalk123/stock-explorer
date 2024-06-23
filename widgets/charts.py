import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

FONT_PATH = 'fonts/GenShinGothic-Monospace-Regular.ttf'


def yaxis_fraction(ax):
    yfmt = ticker.ScalarFormatter(useMathText=True)
    yfmt.set_powerlimits((3, 4))
    ax.yaxis.set_major_formatter(yfmt)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    ax.get_yaxis().get_offset_text().set_visible(False)
    ax_max = max(ax.get_yticks())
    exponent_axis = np.floor(np.log10(ax_max)).astype(int)
    ax.annotate(
        r'$\times$10$^{%i}$' % (exponent_axis),
        xy=(0, .875),
        xycoords='axes fraction', fontsize=9)


class ChartAbstract(FigureCanvas):
    def __init__(self):
        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)

        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 14

        # fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure()

        super().__init__(self.fig)

    def clearAxes(self):
        pass

    def refreshDraw(self):
        pass


class Trend(ChartAbstract):
    def __init__(self, gtype='Candle'):
        super().__init__()
        self.ax = None
        self.ax2 = None

        if gtype == 'Candle':
            self.initCandleStick()
        else:
            self.initTrend()

    def initCandleStick(self):
        grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.0)
        self.ax = self.fig.add_subplot(grid[0:2, 0])
        self.ax2 = self.fig.add_subplot(grid[2, 0], sharex=self.ax)
        self.gtype = 'Candle'

    def initTrend(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.tick_params(axis='x', labelsize=12)
        self.gtype = 'Trend'

    def clearAxes(self):
        if self.gtype == 'Candle':
            self.ax.cla()
            self.ax2.cla()
        else:
            self.ax.cla()

    def getType(self) -> str:
        return self.gtype

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()
        self.gtype = None


class ChartRealtime(ChartAbstract):
    def __init__(self):
        super().__init__()
        self.ax = None

        self.initTrend()

    def initTrend(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.tick_params(axis='x', labelsize=12)

    def clearAxes(self):
        self.ax.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()


class ChartForAnalysis(ChartAbstract):
    def __init__(self):
        super().__init__()
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 8

        self.ax1 = None
        self.ax2 = None
        self.ax3 = None

        self.initTrend()

    def initTrend(self):
        self.fig.subplots_adjust(
            top=0.98,
            bottom=0.1,
            left=0.07,
            right=0.995,
            hspace=0,
        )
        self.ax1 = self.fig.add_subplot(5, 1, (1, 3))  # 5x1の1つめと2つめと3つめ
        self.ax2 = self.fig.add_subplot(5, 1, 4)  # 5x2の4つめ
        self.ax3 = self.fig.add_subplot(5, 1, 5)  # 5x3の5つめ

        self.ax2.sharex(self.ax1)
        self.ax3.sharex(self.ax1)

    def clearAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()


class ChartForVerify01(ChartAbstract):
    def __init__(self):
        super().__init__()
        self.fig.subplots_adjust(
            top=0.98,
            bottom=0.1,
            left=0.07,
            right=0.995,
            hspace=0,
        )
        self.ax1 = self.fig.add_subplot(2, 1, 1)
        self.ax2 = self.fig.add_subplot(2, 1, 2)

        self.ax1.tick_params(axis='x', labelsize=10)
        self.ax1.tick_params(axis='y', labelsize=10)

        self.ax2.tick_params(axis='x', labelsize=10)
        self.ax2.tick_params(axis='y', labelsize=10)
        self.ax2.sharex(self.ax1)

    def clearAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()
