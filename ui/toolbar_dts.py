from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar

from widgets.buttons import ToolButtonDB


class DTSToolBar(QToolBar):
    dbClicked = Signal()
    def __init__(self):
        super().__init__()

        but_db = ToolButtonDB()
        but_db.clicked.connect(self.dbClicked.emit)
        self.addWidget(but_db)