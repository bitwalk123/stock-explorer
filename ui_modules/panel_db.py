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


class PanelDB(QWidget):
    tab_label = 'データベース'

    def __init__(self):
        super().__init__()
        self.progressbar = None
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)

        name_apply = 'SP_DialogApplyButton'
        icon_apply = get_standard_icon(self, name_apply)

        row = 0
        # データベースの初期化
        lab_init = QLabel('データベースの初期化')
        layout.addWidget(lab_init, row, 0)
        but_init = QPushButton()
        but_init.setIcon(icon_apply)
        but_init.clicked.connect(initialize_db)
        layout.addWidget(but_init, row, 1)

        row += 1
        # 東証から上場企業の一覧を取得
        lab_tse = QLabel('東証上場企業一覧を取得・更新')
        layout.addWidget(lab_tse, row, 0)
        but_tse = QPushButton()
        but_tse.setIcon(icon_apply)
        but_tse.clicked.connect(self.update_tse)
        layout.addWidget(but_tse, row, 1)

        row += 1
        # 過去三年分の株価データを取得・更新
        lab_past3y = QLabel('過去三年分株価データを取得・更新')
        layout.addWidget(lab_past3y, row, 0)
        but_past3y = QPushButton()
        but_past3y.setIcon(icon_apply)
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
