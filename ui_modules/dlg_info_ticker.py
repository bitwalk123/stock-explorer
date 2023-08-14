from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QScrollArea, QWidget, QGridLayout, QLabel, \
    QPlainTextEdit, QFrame

from functions.get_info_ticker import get_info_ticker
from functions.resources import get_standard_icon


class DlgInfoTicker(QDialog):
    def __init__(self, code, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('企業情報 - %s.T' % code)

        name = 'SP_MessageBoxInformation'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)

        info = get_info_ticker(code)
        self.init_ui(info)
        self.resize(600, 600)

    def init_ui(self, info: dict):
        """Initialize UI
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        area = QScrollArea()
        area.setContentsMargins(0, 0, 0, 0)
        area.setWidgetResizable(True)
        layout.addWidget(area)
        base = self.panel_ticker_info(info)
        area.setWidget(base)

        dlg_button = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlg_button)
        bbox.setContentsMargins(0, 0, 0, 0)
        bbox.accepted.connect(self.accept)
        layout.addWidget(bbox)

    def panel_ticker_info(self, info):
        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        layout2 = QGridLayout()
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.setSpacing(0)
        base.setLayout(layout2)
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

            layout2.addWidget(lab_left, row, 0)
            layout2.addWidget(lab_right, row, 1)
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
