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
        self.addWidget(combo_code)

        but_code = ToolButton()
        icon = res.getBuiltinIcon(self, 'DialogApplyButton')
        but_code.setIcon(icon)
        but_code.clicked.connect(self.on_clicked_symbol)
        self.addWidget(but_code)

    def on_clicked_symbol(self):
        symbol = self.combo_code.currentText()
        if len(symbol) == 0:
            dlg = DialogWarning('銘柄コードが入力されていません。')
            dlg.exec()
        else:
            self.enteredSymbol.emit(symbol)
