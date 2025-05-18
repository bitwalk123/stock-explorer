import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from widgets.views import TradeView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 500)

        view = TradeView()
        self.setCentralWidget(view)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
