# Reference
# https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

FONT_PATH = 'fonts/RictyDiminished-Regular.ttf'


class MplCanvas(FigureCanvas):

    def __init__(self):
        fm.fontManager.addfont(FONT_PATH)
        font_prop = fm.FontProperties(fname=FONT_PATH)

        plt.rcParams['font.family'] = font_prop.get_name()
        plt.rcParams['font.size'] = 16

        # fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        # self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

    def clearAxes(self):
        self.axes.cla()

    def refreshDraw(self):
        self.fig.canvas.draw()
