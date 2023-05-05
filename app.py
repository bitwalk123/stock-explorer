import os
import platform
import sys
from os.path import expanduser

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget,
)

from dialogs.config_dialog import DlgConfig
from functions.get_standard_ison import get_standard_icon


class StockExplorer(QMainWindow):
    db = 'stock-explorer.sqlite3'

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Explorer')

        # OS depended
        if platform.system() == 'Windows':
            file_config = 'stock_explorer.ini'
        else:
            file_config = '.stock_explorer'

        # ini file
        self.file_ini = os.path.join(expanduser('~'), file_config)
        print(self.file_ini)
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
        but_conf.setToolTip('このアプリケーションの設定')
        name = 'SP_FileDialogDetailedView'
        icon_conf = get_standard_icon(self, name)
        but_conf.setIcon(icon_conf)
        but_conf.clicked.connect(self.show_conf_dialog)
        toolbar.addWidget(but_conf)

        # Exit application
        but_exit = QToolButton()
        but_exit.setText('Exit')
        but_exit.setToolTip('アプリケーションの終了')
        name = 'SP_BrowserStop'
        icon_exit = get_standard_icon(self, name)
        but_exit.setIcon(icon_exit)
        toolbar.addWidget(but_exit)

    def show_conf_dialog(self):
        dlg = DlgConfig(parent=self)
        dlg.show()


def main():
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
