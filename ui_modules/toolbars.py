from PySide6.QtWidgets import (
    QSizePolicy,
    QToolBar,
    QToolButton,
    QWidget, QLabel, QComboBox,
)

from functions.resources import get_standard_icon
from ui_modules.config_dialog import DlgConfig


class ToolBarMain(QToolBar):
    def __init__(self):
        super().__init__()

        lab_range = QLabel('期間')
        lab_range.setContentsMargins(0, 0, 5, 0)
        self.addWidget(lab_range)

        combo_range = QComboBox()
        self.addWidget(combo_range)

        # 余白のスペーサ
        hpad = QWidget()
        hpad.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.addWidget(hpad)

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
