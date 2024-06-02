from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QStyle,
    QToolBar,
    QToolButton,
)


class DTAToolBar(QToolBar):
    clickedClear = Signal()
    clickedOpen = Signal()
    clickedPlot = Signal()

    def __init__(self):
        super().__init__()

        but_open = QToolButton()
        name = 'SP_DirIcon'
        icon = self.get_pixmap_icon(name)
        but_open.setIcon(icon)
        but_open.setToolTip('Open file')
        but_open.clicked.connect(self.on_open)
        self.addWidget(but_open)

        but_plot = QToolButton()
        name = 'SP_MediaPlay'
        icon = self.get_pixmap_icon(name)
        but_plot.setIcon(icon)
        but_plot.setToolTip('Plot data')
        but_plot.clicked.connect(self.on_plot)
        self.addWidget(but_plot)

        but_clear = QToolButton()
        name = 'SP_DialogResetButton'
        icon = self.get_pixmap_icon(name)
        but_clear.setIcon(icon)
        but_clear.setToolTip('Clear data')
        but_clear.clicked.connect(self.on_clear)
        self.addWidget(but_clear)

    def get_pixmap_icon(self, name: str) -> QIcon:
        pixmap_icon = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap_icon)
        return icon

    def on_clear(self):
        self.clickedClear.emit()

    def on_open(self):
        self.clickedOpen.emit()

    def on_plot(self):
        self.clickedPlot.emit()
