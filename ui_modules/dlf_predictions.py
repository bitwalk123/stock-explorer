from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTabWidget,
    QVBoxLayout,
)

from functions.get_standard_icon import get_standard_icon


class DlgPredictions(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle('予測値')

        name = 'SP_FileDialogContentsView'
        icon_win = get_standard_icon(self, name)
        self.setWindowIcon(icon_win)
        self.init_ui()

    def init_ui(self):
        """Initialize UI
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        tab = QTabWidget()
        layout.addWidget(tab)

        #panel_contract = TabPanelContract()
        #panel_database = TabPanelDatabase()
        #tab.addTab(panel_contract, panel_contract.getTabLabel())
        #tab.addTab(panel_database, panel_database.getTabLabel())

        dlg_button = QDialogButtonBox.StandardButton.Ok
        bbox = QDialogButtonBox(dlg_button)
        bbox.setContentsMargins(0, 0, 0, 0)
        bbox.accepted.connect(self.accept)
        layout.addWidget(bbox)
