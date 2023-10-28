from ui_modules.panel_abstract import TabPanelAbstract


class TabPanelContract(TabPanelAbstract):
    tab_label = '約定'

    def __init__(self):
        super().__init__()
