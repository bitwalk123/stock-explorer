from PySide6.QtWidgets import QStyle, QWidget


class AppRes:
    dir_font = 'fonts'
    dir_image = 'images'

    def getBuiltinIcon(self, parent: QWidget, name: str):
        pixmap_icon = getattr(QStyle.StandardPixmap, 'SP_%s' % name)
        return parent.style().standardIcon(pixmap_icon)
