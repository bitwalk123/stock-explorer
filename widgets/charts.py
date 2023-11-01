# Reference
# https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

FONT_PATH = 'fonts/RictyDiminished-Regular.ttf'


class Trend(FigureCanvas):

    def __init__(self):
        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)

        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 16

        # fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure()
        # self.ax = self.fig.add_subplot(111)
        grid = plt.GridSpec(3, 1, wspace=0, hspace=0.0)
        self.ax1 = self.fig.add_subplot(grid[0:2, 0])
        self.ax2 = self.fig.add_subplot(grid[2, 0], sharex=self.ax1)

        self.ax1.tick_params(axis='x', labelsize=12)
        self.ax2.tick_params(axis='x', labelsize=12)

        super().__init__(self.fig)

    def clearAxes(self):
        """Clear Axes
        """
        # self.ax.cla()
        self.ax1.cla()
        self.ax2.cla()

    def refreshDraw(self):
        """Refresh drawn area
        """
        self.fig.canvas.draw()
