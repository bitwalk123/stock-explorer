from PySide6.QtWidgets import QToolBar

from widgets.buttons import ToolButtonDB


class DTSToolBar(QToolBar):
    def __init__(self):
        super().__init__()

        but_db = ToolButtonDB()
        self.addWidget(but_db)