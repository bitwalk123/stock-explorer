import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget,
)

from functions.get_standard_ison import get_standard_icon

db = 'stock-explorer.sqlite3'


class StockExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Explorer')
        self.init_ui()

    def init_ui(self):
        # Create pyqt toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # spacer
        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        toolbar.addWidget(spacer)

        # Application config.
        but_conf = QToolButton()
        but_conf.setText('Configuration')
        but_conf.setToolTip('Configure application setting.')
        name = 'SP_FileDialogDetailedView'
        icon_conf = get_standard_icon(self, name)
        but_conf.setIcon(icon_conf)
        toolbar.addWidget(but_conf)

        # Exit application
        but_exit = QToolButton()
        but_exit.setText('Exit')
        but_exit.setToolTip('Exit application.')
        name = 'SP_BrowserStop'
        icon_exit = get_standard_icon(self, name)
        but_exit.setIcon(icon_exit)
        toolbar.addWidget(but_exit)


def main():
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
