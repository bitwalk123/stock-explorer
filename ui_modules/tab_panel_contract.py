from PySide6.QtWidgets import QLabel, QFileDialog

from functions.read_csv import read_csv_contract_from_shiftjis
from ui_modules.panel_abstract import TabPanelAbstract
from widgets.buttons import ButtonIcon
from widgets.layout import GridLayout


class TabPanelContract(TabPanelAbstract):
    tab_label = '約定'

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = GridLayout()
        self.setLayout(layout)

        row = 0
        # データベースの初期化
        lab_read = QLabel('取引注文ファイルの読み込み')
        layout.addWidget(lab_read, row, 0)
        but_read = ButtonIcon('SP_DirIcon')
        but_read.clicked.connect(self.on_read_clicked)
        layout.addWidget(but_read, row, 1)

    def on_read_clicked(self):
        # _____________________________________________________________________
        # Dialog
        selection = QFileDialog.getOpenFileName(
            parent=self,
            caption='取引注文ファイルの選択',
            filter='CSV File (*.csv)',
        )

        csvfile = selection[0]
        if len(csvfile) == 0:
            return

        print(csvfile)
        read_csv_contract_from_shiftjis(csvfile)
