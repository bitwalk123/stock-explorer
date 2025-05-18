from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QToolBar

from structs.res import AppRes
from widgets.buttons import ToolButton
from widgets.combos import ComboBox
from widgets.dialogs import DialogWarning
from widgets.labels import LabelCode


class ToolBarMain(QToolBar):
    enteredSymbol = Signal(str)

    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

        lab_code = LabelCode('銘柄コード')
        self.addWidget(lab_code)

        self.combo_code = combo_code = ComboBox()
        combo_code.setEditable(True)
        combo_code.setInsertPolicy(ComboBox.InsertPolicy.InsertAlphabetically)
        combo_code.textActivated.connect(self.on_text_activated)
        self.addWidget(combo_code)

    def on_text_activated(self, symbol: str):
        self.enteredSymbol.emit(symbol)
