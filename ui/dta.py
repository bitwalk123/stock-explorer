from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolBar, QToolButton, QStyle


class DTAToolBar(QToolBar):
    clickedOpen = Signal()

    def __init__(self):
        super().__init__()

        but_open = QToolButton()
        name = 'SP_DirIcon'
        icon = self.get_pixmap_icon(name)
        print(type(icon))
        but_open.setIcon(icon)
        but_open.clicked.connect(self.on_open)
        self.addWidget(but_open)

    def get_pixmap_icon(self, name: str) -> QIcon:
        pixmap_icon = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap_icon)
        return icon

    def on_open(self):
        self.clickedOpen.emit()
