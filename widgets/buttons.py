from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QPushButton,
    QRadioButton, QStyle,
)

from functions.get_standard_icon import get_standard_icon


class ApplyButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        name_apply = 'SP_DialogApplyButton'
        icon_apply = get_standard_icon(self, name_apply)
        self.setIcon(icon_apply)


class ButtonIcon(QPushButton):
    """Button with Icon

    Args:
        name_icon(str):name of builtin icon
    """

    def __init__(self, name_icon: str):
        super().__init__()
        pixmap = getattr(QStyle.StandardPixmap, name_icon)
        icon = QIcon(self.style().standardIcon(pixmap))
        self.setIcon(icon)


class TickerRadioButton(QRadioButton):
    def __init__(self, *args):
        super().__init__(*args)

    def setPredicted(self):
        self.setStyleSheet("""
            QRadioButton {
                color: #800000;
                background-color: #FFE0E0;
            }
        """)
