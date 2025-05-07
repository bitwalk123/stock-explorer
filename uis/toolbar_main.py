from PySide6.QtCore import Signal
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
        self.addWidget(combo_code)
        # QShortcut(QKeySequence(Qt.Key.Key_Return), combo_code, self.on_clicked_code)

        but_code = ToolButton()
        icon = res.getBuiltinIcon(self, 'DialogApplyButton')
        but_code.setIcon(icon)
        but_code.clicked.connect(self.on_clicked_code)
        self.addWidget(but_code)

    def on_clicked_code(self):
        code = self.combo_code.currentText()
        if len(code) == 0:
            dlg = DialogWarning('銘柄コードが入力されていません。')
            dlg.exec()
        else:
            symbol = '%s.T' % code
            self.enteredSymbol.emit(symbol)
