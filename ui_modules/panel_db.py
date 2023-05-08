from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QWidget, QProgressDialog,
)

from database.schema import initialize_db
from database.ticker import DBTblTicker
from functions.resources import get_standard_icon
from widgets.buttons import ApplyButton


class PanelDB(QWidget):
    tab_label = 'データベース'

    def __init__(self):
        super().__init__()
        self.progressbar = None
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
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
        lab_tse = QLabel('東証上場企業一覧を取得・更新')
        layout.addWidget(lab_tse, row, 0)
        but_tse = ApplyButton()
        but_tse.clicked.connect(self.update_tse)
        layout.addWidget(but_tse, row, 1)

        row += 1
        # 過去三年分の株価データを取得・更新
        lab_past3y = QLabel('過去三年分の株価データを取得・更新')
        layout.addWidget(lab_past3y, row, 0)
        but_past3y = ApplyButton()
        layout.addWidget(but_past3y, row, 1)

    def getTabLabel(self) -> str:
        return self.tab_label

    def update_progress(self, progress: int):
        self.progressbar.setValue(progress)

    def update_tse(self):
        obj = DBTblTicker(self)
        obj.updateProgress.connect(self.update_progress)
        obj.update()

        # QProgressDialog
        self.progressbar = QProgressDialog(parent=self)
        self.progressbar.setWindowModality(Qt.WindowModal)
        self.progressbar.setCancelButton(None)
        self.progressbar.setWindowTitle('進捗')
        self.progressbar.setLabelText('東証上場企業一覧を取得・更新中')
        self.progressbar.show()
