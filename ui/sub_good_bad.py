import os

from PySide6.QtCore import Signal
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QStatusBar,
    QTabWidget,
)

from models.tables import ModelDataFrame
from structs.res import AppRes
from widgets.tables import TableView


class SubGoodBad(QMainWindow):
    codeSelected = Signal(str)

    def __init__(self, dict_df: dict):
        super().__init__()
        self.dict_df = dict_df
        res = AppRes()

        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        self.setFont(font)

        self.statusbar: QStatusBar | None = None
        self.tab: QTabWidget | None = None
        self.init_ui()

        icon = QIcon(os.path.join(res.getImagePath(), 'fire.png'))
        self.setWindowIcon(icon)
        self.setWindowTitle('好悪材料')
        self.resize(800, 600)

    def init_ui(self):
        self.tab = tab = QTabWidget()
        self.setCentralWidget(tab)

        # 好材料、悪材料…
        for key in self.dict_df.keys():
            view = TableView(key)
            df = self.dict_df[key]
            model = ModelDataFrame(df)
            view.setModel(model)
            vheader = view.verticalHeader()
            vheader.sectionDoubleClicked.connect(self.on_vertical_header_clicked)
            tab.addTab(view, view.getLabel())

        self.statusbar = statusbar = QStatusBar()
        self.setStatusBar(statusbar)

    def on_vertical_header_clicked(self, row: int):
        idx = self.tab.currentIndex()
        key = list(self.dict_df.keys())[idx]
        df = self.dict_df[key]
        series = df.iloc[row]
        code = series['コード']
        self.codeSelected.emit(code)

    def setDlgTitle(self, list_timestamp: list):
        title = '[%s-%s-%s] 大引け後の開示情報からの好悪材料' % (
            list_timestamp[0],
            list_timestamp[1],
            list_timestamp[2],
        )
        self.setWindowTitle(title)
