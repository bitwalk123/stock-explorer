from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPlainTextEdit,
    QScrollArea,
    QWidget,
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
            lab_left = self.handle_header(key)

            if key == 'website':
                lab_right = self.handle_website(info[key])
            elif key == 'longBusinessSummary':
                lab_right = self.handle_long_business_summary(info[key])
            elif key == 'companyOfficers':
                lab_right = self.handle_company_officers(info[key])
            else:
                lab_right = self.handle_general(info[key])

            layout.addWidget(lab_left, row, 0)
            layout.addWidget(lab_right, row, 1)
            row += 1
        return base

    def handle_header(self, value_str) -> QLabel:
        lab = QLabel(value_str)
        lab.setContentsMargins(0, 0, 0, 0)
        lab.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
        lab.setAlignment(Qt.AlignmentFlag.AlignTop)
        lab.setStyleSheet('QLabel {padding:0 2px;}')
        return lab

    def handle_website(self, value) -> QLabel:
        lab = QLabel()
        lab.setText('<a href="%s">%s</a>' % (value, value))
        lab.setOpenExternalLinks(True)
        lab.setContentsMargins(0, 0, 0, 0)
        lab.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab.setStyleSheet('QLabel {padding:0 2px;}')
        return lab

    def handle_long_business_summary(self, value) -> QPlainTextEdit:
        tedit = QPlainTextEdit(str(value))
        tedit.setStyleSheet('QPlainTextEdit {padding:0 2px;}')
        return tedit

    def handle_company_officers(self, value):
        lab = QLabel()
        return lab

    def handle_general(self, value) -> QLabel:
        lab = QLabel(str(value))
        lab.setContentsMargins(0, 0, 0, 0)
        lab.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab.setStyleSheet('QLabel {padding:0 2px;}')
        return lab
