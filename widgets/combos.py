from PySide6.QtWidgets import QComboBox


class ComboTradeRange(QComboBox):
    def __init__(self):
        super().__init__()
        self.addItems(['３ヵ月', '６ヵ月', '１年', '２年', '全て'])
        self.setCurrentText('１年')

