import os
import re

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QPushButton,
    QSizePolicy,
    QStyle,
    QToolButton,
)

from structs.res import AppRes


class JPXCheckBox(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setText('JPX')
        self.setChecked(True)
        self.setContentsMargins(0, 0, 0, 0)


class TickerButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCheckable(True)
        self.setContentsMargins(0, 0, 0, 0)


class TradingButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.func = None
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.setStyleSheet("""
            TradingButton {
                font-family: monospace;
            }        
            TradingButton:disabled {
                color: #888;
                background-color: #ddd;
            }
        """)
        self.setEnabled(False)

    def setFunc(self, func: str):
        self.func = func
        if func == 'login':
            self.setStyleSheet(self.cssLogin())
        elif func == 'domestic':
            self.setStyleSheet(self.cssDomestic())
        elif func == 'search':
            self.setStyleSheet(self.cssSearch())
        elif func == 'buynew':
            self.setStyleSheet(self.cssBuyNew())
        elif func == 'long':
            self.setStyleSheet(self.cssLong())
        elif func == 'short':
            self.setStyleSheet(self.cssShort())
        elif func == 'order':
            self.setStyleSheet(self.cssOrder())

    def getFunc(self, func: str) -> str:
        return self.func

    def cssBuyNew(self) -> str:
        return """
            TradingButton {
                color: white;
                background-color: #a762df;
                font-family: monospace;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    def cssLogin(self) -> str:
        return """
            TradingButton {
                color: white;
                background-color: #bf0000;
                font-family: monospace;
                font-weight: bold;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    def cssDomestic(self) -> str:
        return """
            TradingButton {
                color: #212;
                background-color: #fef;
                font-family: monospace;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    def cssLong(self) -> str:
        return """
            TradingButton {
                color: #008;
                background-color: #ddf;
                font-family: monospace;
                padding: 0.25em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    def cssOrder(self) -> str:
        return """
            TradingButton {
                color: #121;
                background-color: #efe;
                font-family: monospace;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    def cssSearch(self) -> str:
        return """
            TradingButton {
                color: white;
                background-color: #6385cd;
                font-family: monospace;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    def cssShort(self) -> str:
        return """
            TradingButton {
                color: #800;
                background-color: #fdd;
                font-family: monospace;
                padding: 0.25em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """


class IndexButton(TickerButton):
    pattern = re.compile(r'^\^(.+)$')

    def __init__(self, iticker: str):
        super().__init__()
        self.iticker = iticker
        m = self.pattern.match(iticker)
        if m:
            self.setText(m.group(1))
        else:
            self.setText(iticker)

    def getText(self):
        return self.iticker


class LockButton(QPushButton):
    def __init__(self):
        super().__init__()
        res = AppRes()
        self.setCheckable(True)
        self.setChecked(True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        icon_lock = QIcon(os.path.join(res.getImagePath(), 'lock.png'))
        self.setIcon(icon_lock)


class ToolButton(QToolButton):
    def __init__(self, pixmap: str, tooltip: str):
        super().__init__()
        icon = self.get_pixmap_icon(pixmap)
        self.setIcon(icon)
        self.setToolTip(tooltip)

    def get_pixmap_icon(self, name: str) -> QIcon:
        pixmap_icon = getattr(QStyle.StandardPixmap, name)
        icon = self.style().standardIcon(pixmap_icon)
        return icon


class ToolButtonIcon(QToolButton):
    def __init__(self, name_icon: str, tooltip: str):
        super().__init__()
        res = AppRes()
        icon = QIcon(os.path.join(res.getImagePath(), name_icon))
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setToolTip(tooltip)

class ToolButtonDB(ToolButtonIcon):
    def __init__(self, tooltip='Database access'):
        name_icon = 'db.png'
        super().__init__(name_icon, tooltip)
