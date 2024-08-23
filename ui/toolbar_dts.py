from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar

from widgets.buttons import ToolButtonFolder


class DTSToolBar(QToolBar):
    dbClicked = Signal()
    folderClicked = Signal()

    def __init__(self):
        super().__init__()

        """
        but_db = ToolButtonDB()
        but_db.clicked.connect(self.dbClicked.emit)
        self.addWidget(but_db)
        """

        but_folder = ToolButtonFolder()
        but_folder.clicked.connect(self.folderClicked.emit)
        self.addWidget(but_folder)
