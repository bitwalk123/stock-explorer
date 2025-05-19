from PySide6.QtGui import QFont, QPixmap


def get_font_monospace(fsize=10):
    font = QFont('Ricty Diminished')
    font.setPointSize(fsize)
    font.setStyleHint(QFont.StyleHint.Monospace)  # モノスペースフォントを明示的に指定
    return font
