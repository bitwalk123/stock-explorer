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
