import sys

from PySide6.QtWidgets import (
    QApplication,
    QTabWidget,
)


class StockExplorer(QTabWidget):
    __version__ = '0.4.0'

    def __init__(self):
        super().__init__()


def main():
    app = QApplication(sys.argv)
    win = StockExplorer()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
