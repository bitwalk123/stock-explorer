import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from structs.res import AppRes
from widgets.toolbar import ToolBarTick
from widgets.views import TickView


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.res = res = AppRes()
        self.resize(1000, 500)

        toolbar = ToolBarTick(res)
        toolbar.fileSelected.connect(self.on_file_selected)
        self.addToolBar(toolbar)

        view = TickView()
        self.setCentralWidget(view)

    def on_file_selected(self, file_excel: str):
        print(file_excel)


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
