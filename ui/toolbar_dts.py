from PySide6.QtCore import Signal
from PySide6.QtWidgets import QToolBar

from widgets.buttons import ToolButtonFolder, ToolButtonPlay


class DTSToolBar(QToolBar):
    dbClicked = Signal()
    folderClicked = Signal()
    playClicked = Signal()

    def __init__(self):
        super().__init__()

        but_folder = ToolButtonFolder()
        but_folder.clicked.connect(self.folderClicked.emit)
        self.addWidget(but_folder)

        but_start = ToolButtonPlay()
        but_folder.clicked.connect(self.playClicked.emit)
        self.addWidget(but_start)
