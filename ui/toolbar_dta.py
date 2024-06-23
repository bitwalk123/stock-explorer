from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QToolBar, QComboBox,
)

from widgets.buttons import ToolButton, ToolButtonIcon


class DTAToolBar(QToolBar):
    checkChanged = Signal()
    clickedBack = Signal()
    clickedClear = Signal()
    clickedForward = Signal()
    clickedOpen = Signal()
    clickedPlot = Signal()

    def __init__(self):
        super().__init__()
        # res = AppRes()

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

        # pixmap = 'SP_DialogResetButton'
        name_icon = 'eraser.png'
        tooltip = 'Clear data'
        but_clear = ToolButtonIcon(name_icon, tooltip)
        but_clear.clicked.connect(self.on_clear)
        self.addWidget(but_clear)

        self.addSeparator()

        self.cb_robust = cb_robust = QCheckBox('Robust')
        cb_robust.setChecked(False)
        cb_robust.checkStateChanged.connect(self.on_check_changed)
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

    def isRobust(self) -> bool:
        return self.cb_robust.isChecked()

    def on_back(self):
        self.clickedBack.emit()

    def on_check_changed(self, state):
        self.checkChanged.emit()

    def on_clear(self):
        self.clickedClear.emit()

    def on_forward(self):
        self.clickedForward.emit()

    def on_open(self):
        self.clickedOpen.emit()

    def on_plot(self):
        self.clickedPlot.emit()


class DTAVerifyToolBar(QToolBar):
    clickedStart = Signal()

    def __init__(self):
        super().__init__()

        self.combo = combo = QComboBox()
        combo.addItems(['8035', '7735', '6920', '6857', '6525', '6146'])
        self.addWidget(combo)

        pixmap = 'SP_MediaPlay'
        tooltip = 'Start verification'
        but_start = ToolButton(pixmap, tooltip)
        but_start.clicked.connect(self.on_start)
        self.addWidget(but_start)

    def getTicker(self) -> str:
        return self.combo.currentText()

    def on_start(self):
        self.clickedStart.emit()
