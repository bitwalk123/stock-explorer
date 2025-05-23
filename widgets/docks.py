from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QWidget,
)

from structs.res import AppRes
from widgets.buttons import ButtonSave
from widgets.container import Widget, PadH
from widgets.labels import LCDNumber
from widgets.layouts import HBoxLayout, VBoxLayout


class DockTrader(QDockWidget):
    saveClicked = Signal()

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        self.setFeatures(
            QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
        )

        base = QWidget()
        self.setWidget(base)

        layout = VBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        base.setLayout(layout)

        self.lcd_price = lcd_price = LCDNumber(self)
        layout.addWidget(lcd_price)

        self.lcd_profit = lcd_profit = LCDNumber(self)
        layout.addWidget(lcd_profit)

        self.lcd_total = lcd_total = LCDNumber(self)
        layout.addWidget(lcd_total)

        row_tool = Widget()
        layout.addWidget(row_tool)

        layout_tool = HBoxLayout()
        row_tool.setLayout(layout_tool)

        pad = PadH()
        layout_tool.addWidget(pad)

        but_save = ButtonSave()
        but_save.clicked.connect(self.on_save)
        layout_tool.addWidget(but_save)

    def on_save(self):
        # ---------------------------------
        # 🧿 保存ボタンがクリックされたことを通知
        # ---------------------------------
        self.saveClicked.emit()

    def setPrice(self, price: float):
        self.lcd_price.display(f"{price:.1f}")
