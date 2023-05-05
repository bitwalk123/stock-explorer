from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QStyle


def get_standard_icon(parent: QObject, name_pixmap: str) -> QIcon:
    """
    get Standard Pixmap and convert QIcon instance

    Args:
        parent(QObject): Parent instance inheriting from the QObject.
        name_pixmap(str): name of standard picmap
    
    Returns:
        QIcon: instance of QIcon of specified pixmap
    """
    pixmap = getattr(QStyle.StandardPixmap, name_pixmap)
    icon = parent.style().standardIcon(pixmap)

    return icon
