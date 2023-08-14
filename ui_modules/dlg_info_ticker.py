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

        base = QWidget()
        base.setContentsMargins(0, 0, 0, 0)
        area.setWidget(base)

        layout2 = QGridLayout()
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.setSpacing(0)
        base.setLayout(layout2)

        row = 0
        for key in info.keys():
            lab_left = QLabel(key)
            lab_left.setContentsMargins(0, 0, 0, 0)
            lab_left.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Raised)
            lab_left.setAlignment(Qt.AlignmentFlag.AlignTop)
            lab_left.setStyleSheet('QLabel {padding:0 2px;}')

            if key == 'website':
                lab_right = QLabel()
                lab_right.setText('<a href="%s">%s</a>' % (info[key], info[key]))
                lab_right.setOpenExternalLinks(True)
                lab_right.setContentsMargins(0, 0, 0, 0)
                lab_right.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
                lab_right.setStyleSheet('QLabel {padding:0 2px;}')
            elif key == 'longBusinessSummary':
                lab_right = QPlainTextEdit(str(info[key]))
                lab_right.setStyleSheet('QPlainTextEdit {padding:0 2px;}')
            elif key == 'companyOfficers':
                lab_right = QLabel()
            else:
                lab_right = self.handle_general(str(info[key]))

            layout2.addWidget(lab_left, row, 0)
            layout2.addWidget(lab_right, row, 1)
            row += 1

        dlg_button = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlg_button)
        bbox.setContentsMargins(0, 0, 0, 0)
        bbox.accepted.connect(self.accept)
        layout.addWidget(bbox)

    def handle_general(self, value: str) -> QLabel:
        lab_right = QLabel(value)
        lab_right.setContentsMargins(0, 0, 0, 0)
        lab_right.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        lab_right.setStyleSheet('QLabel {padding:0 2px;}')
        return lab_right
