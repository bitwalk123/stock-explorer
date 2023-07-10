from PySide6.QtWidgets import QWidget, QSizePolicy, QMainWindow
from matplotlib_inline.backend_inline import FigureCanvas


class WinPlot(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        #self.setSizePolicy(
        #    QSizePolicy.Policy.Expanding,
        #    QSizePolicy.Policy.Expanding
        #)
