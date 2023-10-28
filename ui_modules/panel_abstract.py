from PySide6.QtWidgets import QWidget


class TabPanelAbstract(QWidget):
    tab_label = ''

    def __init__(self):
        super().__init__()

    def getTabLabel(self) -> str:
        return self.tab_label
