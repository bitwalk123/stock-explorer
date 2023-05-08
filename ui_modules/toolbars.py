from PySide6.QtWidgets import QToolBar, QWidget, QSizePolicy, QToolButton

from functions.resources import get_standard_icon
from ui_modules.config_dialog import DlgConfig


class ToolBarMain(QToolBar):
    def __init__(self):
        super().__init__()

        # 余白のスペーサ
        spacer = QWidget()
        spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.addWidget(spacer)

        # Application config.
        but_conf = QToolButton()
        but_conf.setText('Configuration')
        but_conf.setToolTip('このアプリケーションの設定')
        name = 'SP_FileDialogDetailedView'
        icon_conf = get_standard_icon(self, name)
        but_conf.setIcon(icon_conf)
        but_conf.clicked.connect(self.show_conf_dialog)
        self.addWidget(but_conf)

    def show_conf_dialog(self):
        dlg = DlgConfig(parent=self)
        dlg.show()
