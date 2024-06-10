from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar, QCheckBox

from widgets.buttons import ToolButton


class DTAToolBar(QToolBar):
    clickedBack = Signal()
    clickedClear = Signal()
    clickedForward = Signal()
    clickedOpen = Signal()
    clickedPlot = Signal()

    def __init__(self):
        super().__init__()

        pixmap = 'SP_DirIcon'
        tooltip = 'Open file'
        but_open = ToolButton(pixmap, tooltip)
        but_open.clicked.connect(self.on_open)
        self.addWidget(but_open)

        pixmap = 'SP_MediaPlay'
        tooltip = 'Plot data'
        but_plot = ToolButton(pixmap, tooltip)
        but_plot.clicked.connect(self.on_plot)
        self.addWidget(but_plot)

        pixmap = 'SP_DialogResetButton'
        tooltip = 'Clear data'
        but_clear = ToolButton(pixmap, tooltip)
        but_clear.clicked.connect(self.on_clear)
        self.addWidget(but_clear)

        self.addSeparator()

        self.cb_robust = cb_robust = QCheckBox('Robust')
        cb_robust.setChecked(True)
        self.addWidget(cb_robust)

        self.addSeparator()

        pixmap = 'SP_ArrowBack'
        tooltip = 'Previous data'
        but_back = ToolButton(pixmap, tooltip)
        but_back.clicked.connect(self.on_back)
        self.addWidget(but_back)

        pixmap = 'SP_ArrowForward'
        tooltip = 'Next data'
        but_forward = ToolButton(pixmap, tooltip)
        but_forward.clicked.connect(self.on_forward)
        self.addWidget(but_forward)

    def on_back(self):
        self.clickedBack.emit()

    def on_clear(self):
        self.clickedClear.emit()

    def on_forward(self):
        self.clickedForward.emit()

    def on_open(self):
        self.clickedOpen.emit()

    def on_plot(self):
        self.clickedPlot.emit()
