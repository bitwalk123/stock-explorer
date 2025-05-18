import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QToolButton

from structs.res import AppRes


class FolderToolButton(QToolButton):
    def __init__(self, res: AppRes):
        super().__init__()
        self.setIcon(
            QIcon(os.path.join(res.dir_image, 'folder.png'))
        )


class Button(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QPushButton {font-family: monospace;}')


class ToolButton(QToolButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QToolButton {font-family: monospace;}')
