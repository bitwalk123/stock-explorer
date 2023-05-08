import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget,
)

from ui_modules.config_dialog import DlgConfig
from functions.resources import get_standard_icon, get_ini_file


class StockExplorer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Stock Explorer')

        self.file_ini = get_ini_file()
        print(self.file_ini)

        self.init_ui()

    def init_ui(self):
        # ツールバー
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 余白のスペーサ
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

    def show_conf_dialog(self):
        dlg = DlgConfig(parent=self)
        dlg.show()

    def closeEvent(self, event):
        """Close event when user click X button.
        """
        print('アプリケーションを終了します。')
        event.accept()  # let the window close


def main():
    app = QApplication(sys.argv)
    obj = StockExplorer()
    obj.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
