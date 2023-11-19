from PySide6.QtCore import (
    QSize,
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from functions.get_predict import (
    get_predict_dataframe,
    get_predict_date_latest,
)
from ui_modules.panel_abstract import TabPanelAbstract
from widgets.labels import LabelDate, LabelFlat
from widgets.tables import TblPredict
from widgets.widgets import HPad


class TabPanelPredict(TabPanelAbstract):
    rowDblClicked = Signal(int)
    tab_label = '始値予測一覧'

    def __init__(self):
        super().__init__()
        self.view = None
        self.setMinimumSize(QSize(700, 500))
        # self.resize(QSize(600, 600))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )
        self.setLayout(layout)

        bar = QWidget()
        layout.addWidget(bar)

        layout_bar = QHBoxLayout()
        layout_bar.setSpacing(0)
        layout_bar.setContentsMargins(0, 0, 0, 0)
        bar.setLayout(layout_bar)

        lab_date_title = LabelFlat('Target Date')
        layout_bar.addWidget(lab_date_title)
        lab_date = LabelDate()
        date_predict = get_predict_date_latest()
        lab_date.setDate(date_predict)
        lab_date.setFixedWidth(100)
        layout_bar.addWidget(lab_date)
        pad = HPad()
        layout_bar.addWidget(pad)

        # Predictions
        df_pred = get_predict_dataframe(date_predict)
        self.view = TblPredict(df_pred)
        header_row = self.view.verticalHeader()
        header_row.sectionDoubleClicked.connect(self.row_double_clicked)
        layout.addWidget(self.view)

    def row_double_clicked(self, row: int):
        code = self.view.get_code(row)
        self.rowDblClicked.emit(code)
