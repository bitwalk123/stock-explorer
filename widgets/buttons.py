import re

from PySide6.QtWidgets import QPushButton, QCheckBox


class JPXCheckBox(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setText('JPX')
        self.setChecked(True)
        self.setContentsMargins(0, 0, 0, 0)


class TickerButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCheckable(True)
        self.setContentsMargins(0, 0, 0, 0)


class TradingButton(QPushButton):
    def __init__(self, *args):
        super().__init__(*args)
        self.func = None
        self.setEnabled(False)

    def setFunc(self, func: str):
        self.func = func

    def getFunc(self, func: str) -> str:
        return self.func


class IndexButton(TickerButton):
    pattern = re.compile(r'^\^(.+)$')

    def __init__(self, iticker: str):
        super().__init__()
        self.iticker = iticker
        m = self.pattern.match(iticker)
        if m:
            self.setText(m.group(1))
        else:
            self.setText(iticker)

    def getText(self):
        return self.iticker
