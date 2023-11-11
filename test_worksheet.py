import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from widgets.worksheet import WorkSheet


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Worksheet test')
        self.init_ui()

    def init_ui(self):
        sheet = WorkSheet()
        self.setCentralWidget(sheet)


def main():
    """Main event loop
    """
    app = QApplication(sys.argv)
    obj = Example()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
