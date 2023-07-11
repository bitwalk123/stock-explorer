# Reference
# https://stackoverflow.com/questions/8213522/when-to-use-cla-clf-or-close-for-clearing-a-plot
# https://www.tutorialspoint.com/how-to-clear-the-memory-completely-of-all-matplotlib-plots
import random
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolBar,
    QToolButton,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def clear_axes(self):
        self.axes.cla()

    def refresh_draw(self):
        self.fig.canvas.draw()


class MainWindow(QMainWindow):
    count = 1

    def __init__(self):
        super().__init__()

        toolbar = QToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbutton = QToolButton()
        toolbutton.setText('TEST')
        toolbutton.clicked.connect(self.toolButtonClicked)
        toolbar.addWidget(toolbutton)

        self.plot = MplCanvas()
        self.draw_plot()
        self.setCentralWidget(self.plot)

        self.show()

    def toolButtonClicked(self):
        self.plot.clear_axes()
        self.draw_plot()
        self.plot.refresh_draw()

    def draw_plot(self):
        list_x = [x for x in range(100)]
        list_y = [(random.random() - 0.5) * 100 for i in range(100)]
        self.plot.axes.plot(list_x, list_y)
        self.plot.axes.set_title('TEST %d' % self.count)
        self.plot.axes.set_xlabel('X')
        self.plot.axes.set_ylabel('Y')
        self.plot.axes.grid()
        self.count += 1


app = QApplication(sys.argv)
w = MainWindow()
app.exec()
