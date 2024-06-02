import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

FONT_PATH = 'fonts/GenShinGothic-Monospace-Regular.ttf'


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
        plt.rcParams['legend.fontsize'] = 8
        self.ax = None

        self.initTrend()

    def initTrend(self):
        self.fig.subplots_adjust(
            top=0.98,
            bottom=0.1,
            left=0.07,
            right=0.995
        )
        self.ax = self.fig.add_subplot(111)

    def clearAxes(self):
        self.ax.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()

    def removeAxes(self):
        axs = self.fig.axes
        for ax in axs:
            ax.remove()
