from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QScrollArea,
    QWidget,
)

from widgets.tables import (
    CellDescription,
    CellGeneral,
    CellHyperLink,
    HeaderTickerInfo,
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
            lab_left = HeaderTickerInfo(key)

            if key == 'website':
                lab_right = CellHyperLink(info[key])
            elif key == 'longBusinessSummary':
                lab_right = CellDescription(info[key])
            elif key == 'companyOfficers':
                #lab_right = self.handle_company_officers(info[key])
                lab_right = CellOfficers(info[key])
            else:
                lab_right = CellGeneral(info[key])

            layout.addWidget(lab_left, row, 0)
            layout.addWidget(lab_right, row, 1)
            row += 1
        return base

    def handle_company_officers(self, value):
        lab = QLabel()
        return lab


class CellOfficers(QScrollArea):
    def __init__(self, list_value: list):
        super().__init__()
        #self.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)


