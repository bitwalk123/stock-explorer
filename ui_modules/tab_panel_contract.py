from PySide6.QtWidgets import QGridLayout, QLabel

from ui_modules.panel_abstract import TabPanelAbstract
from widgets.buttons import ApplyButton


class TabPanelContract(TabPanelAbstract):
    tab_label = '約定'

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        self.setLayout(layout)

        row = 0
        # データベースの初期化
        lab_read = QLabel('取引注文ファイルの読み込み')
        layout.addWidget(lab_read, row, 0)
        but_read = ApplyButton()
        # but_read.clicked.connect()
        layout.addWidget(but_read, row, 1)
