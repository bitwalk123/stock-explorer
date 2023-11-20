import os

from PySide6.QtCore import Qt, Signal, QEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QTabWidget,
    QVBoxLayout,
)

from functions.get_standard_icon import get_standard_icon
from ui_modules.tab_panel_predict import TabPanelPredict


class DlgPredictions(QDialog):
    closeDlg = Signal()
    updateCode = Signal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowTitle('予測値閲覧')

        # name = 'SP_FileDialogContentsView'
        # icon_win = get_standard_icon(self, name)
        # self.setWindowIcon(icon_win)
        icon = QIcon(os.path.join('images', 'predict.png'))
        self.setWindowIcon(icon)

        self.init_ui()

    def closeEvent(self, event):
        """Close event when user click X button.
        """
        self.closeDlg.emit()
        event.accept()  # let the window close

    def init_ui(self):
        """Initialize UI
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        tab = QTabWidget()
        layout.addWidget(tab)

        panel_pred = TabPanelPredict()
        panel_pred.rowDblClicked.connect(self.update_code)
        tab.addTab(panel_pred, panel_pred.getTabLabel())

    def update_code(self, code: int):
        self.updateCode.emit(code)
