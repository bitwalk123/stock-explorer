from PySide6.QtWidgets import QTableView, QHeaderView


class TableView(QTableView):
    def __init__(self, label: str):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.label = label

        # Horizontal header of table
        header = self.horizontalHeader()
        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Row colors
        self.setAlternatingRowColors(True)

    def getLabel(self) -> str:
        return self.label
