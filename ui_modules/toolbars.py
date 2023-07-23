import datetime as dt
import pandas as pd
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget,
)

from functions.resources import get_standard_icon
from ui_modules.config_dialog import DlgConfig


class ToolBarMain(QToolBar):
    periodUpdate = Signal()
    tickerUp = Signal()
    tickerDown = Signal()

    def __init__(self):
        super().__init__()
        self.combo_range = QComboBox()

        self.init_ui()

    def init_ui(self):
        # 期間
        lab_range = QLabel('期間')
        lab_range.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_range)
        self.combo_range.addItems(['１年', '２年', '全て'])
        self.combo_range.currentIndexChanged.connect(self.selected_range_changed)
        self.addWidget(self.combo_range)

        self.addSeparator()

        # Go up ticker
        but_up = QToolButton()
        icon_up = get_standard_icon(self, 'SP_ArrowUp')
        but_up.setIcon(icon_up)
        but_up.clicked.connect(self.on_ticker_up)
        self.addWidget(but_up)

        # Go down ticker
        but_down = QToolButton()
        icon_down = get_standard_icon(self, 'SP_ArrowDown')
        but_down.setIcon(icon_down)
        but_down.clicked.connect(self.on_ticker_down)
        self.addWidget(but_down)

        # 余白のスペーサ
        hpad = QWidget()
        hpad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.addWidget(hpad)

        # Application config.
        but_conf = QToolButton()
        but_conf.setText('Configuration')
        but_conf.setToolTip('このアプリケーションの設定')
        icon_conf = get_standard_icon(self, 'SP_FileDialogDetailedView')
        but_conf.setIcon(icon_conf)
        but_conf.clicked.connect(self.show_conf_dialog)
        self.addWidget(but_conf)

    def get_start_date(self) -> int:
        sel = self.combo_range.currentText()
        today = int(pd.to_datetime(str(dt.date.today())).timestamp())
        year = 365 * 24 * 60 * 60
        if sel == '１年':
            return today - year
        elif sel == '２年':
            return today - 2 * year
        else:
            return -1

    def on_ticker_down(self):
        self.tickerDown.emit()

    def on_ticker_up(self):
        self.tickerUp.emit()

    def selected_range_changed(self, i):
        # print(self.combo_range.itemText(i))
        self.periodUpdate.emit()

    def show_conf_dialog(self):
        dlg = DlgConfig(parent=self)
        dlg.show()
