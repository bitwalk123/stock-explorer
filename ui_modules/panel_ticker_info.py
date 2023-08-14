from PySide6.QtWidgets import (
    QGridLayout,
    QScrollArea,
    QWidget,
)

from widgets.tables import (
    CellDescription,
    CellGeneral,
    CellHyperLink,
    CellOfficers,
    HeaderGeneral,
)


class PanelTickerInfo(QScrollArea):
    def __init__(self, info):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)

        self.init_ui(info)

    def init_ui(self, info):
        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        self.setWidget(base)

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        base.setLayout(layout)

        row = 0
        for key in info.keys():
            lab_left = HeaderGeneral(key)

            if key == 'website':
                lab_right = CellHyperLink(info[key])
            elif key == 'longBusinessSummary':
                lab_right = CellDescription(info[key])
            elif key == 'companyOfficers':
                lab_right = CellOfficers(info[key])
            else:
                lab_right = CellGeneral(info[key])

            layout.addWidget(lab_left, row, 0)
            layout.addWidget(lab_right, row, 1)
            row += 1
