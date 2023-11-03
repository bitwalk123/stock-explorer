from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QProgressDialog, QMessageBox,
)

from database.schema import initialize_db
from database.ticker import DBTblTicker
from database.trade import DBTblTrade
from functions.get_standard_icon import get_standard_icon
from ui_modules.panel_abstract import TabPanelAbstract
from widgets.buttons import ApplyButton
from widgets.dialog import DialogConfirmationYesCancel
from widgets.layout import GridLayout


class TabPanelDatabase(TabPanelAbstract):
    tab_label = 'データベース'

    def __init__(self):
        super().__init__()
        self.progressbar = None
        self.init_ui()

    def init_ui(self):
        layout = GridLayout()
        self.setLayout(layout)

        row = 0
        # データベースの初期化
        lab_init = QLabel('データベースの初期化')
        layout.addWidget(lab_init, row, 0)
        but_init = ApplyButton()
        but_init.clicked.connect(initialize_db)
        layout.addWidget(but_init, row, 1)

        row += 1
        # 東証から上場企業の一覧を取得
        lab_tse = QLabel('東証上場企業一覧を新規作成')
        layout.addWidget(lab_tse, row, 0)
        but_tse = ApplyButton()
        but_tse.clicked.connect(self.update_tse)
        layout.addWidget(but_tse, row, 1)

        row += 1
        # 重複した株価データを削除
        lab_dup = QLabel('重複した株価データを削除')
        layout.addWidget(lab_dup, row, 0)
        but_dup = ApplyButton()
        but_dup.clicked.connect(self.check_duplicate)
        layout.addWidget(but_dup, row, 1)

        """
        row += 1
        lab_update = QLabel('最新の株価データに更新')
        layout.addWidget(lab_update, row, 0)
        but_update = ApplyButton()
        but_update.clicked.connect(self.update_trade)
        layout.addWidget(but_update, row, 1)
        """

    def update_progress(self, progress: int):
        self.progressbar.setValue(progress)

    def update_tse(self):
        dlg = DialogConfirmationYesCancel(parent=self)
        dlg.setText('本当に、東証上場企業一覧を新規に作成して宜しいですか？')
        button = dlg.exec()
        if button == QMessageBox.StandardButton.Cancel:
            print('Canceled to create new ticker table.')
            return

        obj = DBTblTicker(self)
        obj.updateProgress.connect(self.update_progress)
        obj.update()

        # QProgressDialog
        self.progressbar = QProgressDialog(parent=self)
        self.progressbar.setWindowModality(Qt.WindowModal)
        self.progressbar.setCancelButton(None)
        self.progressbar.setWindowTitle('進捗')
        self.progressbar.setLabelText('東証上場企業一覧を取得・作成中')
        self.progressbar.show()

    def check_duplicate(self):
        obj = DBTblTrade(self)
        obj.updateProgress.connect(self.update_progress)
        obj.check_duplicate()

        # QProgressDialog
        self.progressbar = QProgressDialog(parent=self)
        self.progressbar.setWindowModality(Qt.WindowModal)
        self.progressbar.setCancelButton(None)
        self.progressbar.setWindowTitle('進捗')
        self.progressbar.setLabelText('重複した株価データを確認・削除中')
        self.progressbar.show()

    def update_trade(self):
        obj = DBTblTrade(self)
        obj.updateProgress.connect(self.update_progress)
        obj.update_trade()

        # QProgressDialog
        self.progressbar = QProgressDialog(parent=self)
        self.progressbar.setWindowModality(Qt.WindowModal)
        self.progressbar.setCancelButton(None)
        self.progressbar.setWindowTitle('進捗')
        self.progressbar.setLabelText('最新の株価データに更新中')
        self.progressbar.show()
