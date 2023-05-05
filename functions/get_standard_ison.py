from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle


def get_standard_icon(parent: QObject, name: str) -> QIcon:
    pixmap = getattr(QStyle.StandardPixmap, name)
    icon = parent.style().standardIcon(pixmap)
    return icon
