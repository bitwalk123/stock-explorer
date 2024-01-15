from PySide6.QtCore import Qt

from ui.dock_navigator import DockNavigator
from widgets.charts import Trend
from widgets.tab_panels import TabPanelMain


class MainAnalytics(TabPanelMain):
    tab_label = '分析'

    def __init__(self, parent):
        super().__init__(parent)

        self.init_ui()

    def init_ui(self):
        # CandleStick chart as default
        chart = Trend()
        self.setCentralWidget(chart)

        # Bottom Dock
        self.dock_bottom = dock_bottom = DockNavigator(self, chart)
        self.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea,
            dock_bottom
        )
