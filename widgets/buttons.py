import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QToolButton, QStyle

from structs.res import AppRes


class Button(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QPushButton {font-family: monospace;}')


class ButtonSave(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_DialogSaveButton
            )
        )


class ButtonBuy(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("""
            QPushButton {
                font-family: monospace;
                background: #ed6286;
            }
            QPushButton:hover {
                background: #f194a7;
            }
        """)
        self.setText("買建")


class ButtonSell(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("""
            QPushButton {
                font-family: monospace;
                background: #0ba596;
            }
            QPushButton:hover {
                background: #7bbbb1;
            }
        """)
        self.setText("売建")


class ButtonRepay(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet("""
            QPushButton {
                font-family: monospace;
                background: #238fe7;
            }
            QPushButton:hover {
                background: #7eadec;
            }
        """)
        self.setText("返　　済")


class ToolButton(QToolButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setStyleSheet('QToolButton {font-family: monospace;}')


class ToolButtonImage(QToolButton):
    def __init__(self, res: AppRes):
        super().__init__()
        self.res = res

    def setImage(self, name_image: str):
        icon = QIcon(os.path.join(self.res.dir_image, name_image))
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))


class ToolButtonFolder(ToolButtonImage):
    def __init__(self, res: AppRes):
        super().__init__(res)
        self.setImage('folder.png')


class ToolButtonSave(ToolButtonImage):
    def __init__(self, res: AppRes):
        super().__init__(res)
        self.setImage('save.png')
