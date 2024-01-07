from PySide6.QtWidgets import QMainWindow, QWidget


class TabPanelMain(QMainWindow):
    tab_label = ''

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setContentsMargins(0, 0, 0, 0)

    def getTabLabel(self) -> str:
        return self.tab_label


class TabPanelWidget(QWidget):
    tab_label = ''

    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)

    def getTabLabel(self) -> str:
        return self.tab_label
