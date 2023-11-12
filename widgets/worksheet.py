from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)


class WorkSheet(QTableWidget):
    cellUpdated = Signal(QTableWidgetItem)
    css_table = """
        QTableWidget {
            font-family: monospace;
        }
        QTableCornerButton::section {
            background: #fff;
        }
        QHeaderView {
            font-family: monospace;
            background: #eee;
            color: #666;
        }
    """

    def __init__(self, row_max=256, col_max=100):
        super().__init__(row_max, col_max)
        self.setStyleSheet(self.css_table)
        self.enableEvent()

        header_horiz = QHeaderView(Qt.Orientation.Horizontal, parent=self)
        header_horiz.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setHorizontalHeader(header_horiz)

        header_vert = QHeaderView(Qt.Orientation.Vertical, parent=self)
        header_vert.setDefaultAlignment(Qt.AlignmentFlag.AlignRight)
        header_vert.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setVerticalHeader(header_vert)

    def cell_updated(self, item: QTableWidgetItem):
        self.cellUpdated.emit(item)

    def enableEvent(self):
        self.itemChanged.connect(self.cell_updated)

    def disableEvent(self):
        self.itemChanged.disconnect(self.cell_updated)
