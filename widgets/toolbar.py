import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar

from structs.res import AppRes
from widgets.buttons import FolderToolButton
from widgets.combos import ComboBox
from widgets.dialogs import FileDialogExcel
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


class ToolBarTick(QToolBar):
    fileSelected = Signal(str)

    def __init__(self, res: AppRes):

        super().__init__()
        self.res = res

        but_folder = FolderToolButton(res)
        but_folder.setToolTip('ファイル選択')
        but_folder.clicked.connect(self.on_file_dialog_open)
        self.addWidget(but_folder)

    def on_file_dialog_open(self):
        dialog = FileDialogExcel(self.res)
        if not dialog.exec():
            return

        # ----------------------------------
        # 🧿 選択されたファイルが存在して入れば通知
        # ----------------------------------
        file_excel = dialog.selectedFiles()[0]
        if os.path.isfile(file_excel):
            self.fileSelected.emit(file_excel)
