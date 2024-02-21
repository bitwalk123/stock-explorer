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
        self.setStyleSheet("""
            TradingButton {
                font-family: monospace;
            }        
            TradingButton:disabled {
                color: #888;
                background-color: #ddd;
            }
        """)
        self.setEnabled(False)

    def setFunc(self, func: str):
        self.func = func
        if func == 'login':
            self.setStyleSheet(self.cssLogin())
        elif func == 'search':
            self.setStyleSheet(self.cssSearch())
        elif func == 'buynew':
            self.setStyleSheet(self.cssBuyNew())

    def getFunc(self, func: str) -> str:
        return self.func

    def cssBuyNew(self) -> str:
        return """
            TradingButton {
                color: white;
                background-color: #a762df;
                font-family: monospace;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """

    def cssLogin(self) -> str:
        return """
            TradingButton {
                color: white;
                background-color: #bf0000;
                font-family: monospace;
                font-weight: bold;
                padding: 0.5em;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
                font-weight: normal;
            }
        """

    def cssSearch(self) -> str:
        return """
            TradingButton {
                color: white;
                background-color: #6385cd;
                font-family: monospace;
            }        
            TradingButton:disabled {
                color: gray;
                background-color: lightgray;
            }
        """


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
