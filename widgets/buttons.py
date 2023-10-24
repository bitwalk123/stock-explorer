from PySide6.QtWidgets import (
    QPushButton,
    QRadioButton,
)

from functions.get_standard_icon import get_standard_icon


class ApplyButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        name_apply = 'SP_DialogApplyButton'
        icon_apply = get_standard_icon(self, name_apply)
        self.setIcon(icon_apply)


class TickerRadioButton(QRadioButton):
    def __init__(self, *args):
        super().__init__(*args)
